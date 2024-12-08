# 3rd party library imports
from rest_framework.generics import get_object_or_404
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import requests
from requests.exceptions import JSONDecodeError
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from rest_framework.serializers import IntegerField, CharField
from logging import getLogger

# Local imports
from orders.models import Order
from utils.order import get_order_price
from .models import Transaction
from orders.serializers import OrderRetrieveSerializer

logger = getLogger(__name__)

@extend_schema_view(
    get=extend_schema(
        summary="Returns the payment gateway URL for an order",
        description="""Returns the payment gateway URL for a pending order.
        Will return 409 if order price is not up to date.
        For a complete list of gateway errors please visit https://www.zarinpal.com/docs/paymentGateway/
        
        
        This endpoint requires authentication.""",
        responses={
            200: inline_serializer("Gateway URL", {'status_code': IntegerField(max_value=100),
                                    'url':CharField(default='https://sandbox.zarinpal.com/pg/StartPay/{authority}')}),
        }
    )
)
class PaymentInitiatorView(APIView):
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='pending')

    def get_object(self):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=self.kwargs['order_id'])
        return obj

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        current_price = get_order_price(order)

        if order.total_price != current_price:
            order.total_price = current_price
            order.save()
            logger.info(f"Order price has been updated. order id: {order.id}")
            return Response({'Message': 'Order price has been updated. Please try again.'},
                            status=HTTP_409_CONFLICT)

        body = {
            'merchant_id': 'e6543027-9cd8-4811-b660-5c4f4e9a66ad',
            'amount': order.total_price,
            'callback_url': 'http://127.0.0.1:8000/transactions/verify/callback',
            'description': 'random description',
        }
        response = requests.post('https://sandbox.zarinpal.com/pg/v4/payment/request.json', json=body)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['data']['authority']
            code = response_json['data']['code']
            transaction = Transaction(authority=authority, code=code, order=order)
            transaction.save()

            logger.info(f"Payment gateway successfully initiated. transaction id: {transaction.id}, order id: {order.id}")
            return Response({'status_code': code,
                             'url': f'https://sandbox.zarinpal.com/pg/StartPay/{authority}'})
        else:
            try:
                response_json = response.json()
                error = response_json['errors']
            except JSONDecodeError:
                error= 'unknown error'

            logger.error(f"Payment gateway failed to initiate for an order. order id: {order.id}, error: {error}")
            return Response({'status': 'something went wrong',
                             'errors': error})



@extend_schema_view(
    get=extend_schema(
        summary='Handles payment verification.',
        description="""Users would normally not send any requests to this endpoint.
        This is only used by the payment gateway to signal a transactions status."""
    )
)
class PaymentVerifierView(APIView):
    serializer_class = OrderRetrieveSerializer

    def get(self, request, *args, **kwargs):
        status = request.query_params['Status']
        if status == 'OK':
            authority = request.query_params['Authority']
            order = Order.objects.get(transaction__authority=authority)
            body = {
                'merchant_id': 'e6543027-9cd8-4811-b660-5c4f4e9a66ad',
                'amount': order.total_price,
                'authority': authority
            }
            response = requests.post('https://sandbox.zarinpal.com/pg/v4/payment/verify.json', json=body)
            response_json = response.json()
            code = response_json['data']['code']
            if code == 100 or code == 101: # if transaction is verified
                order.status = 'processing'
                order.save()
                serializer = OrderRetrieveSerializer(order)
                serializer.data['message'] = 'Payment successful'

                logger.info(f"Payment verified successfully. order id: {order.id}")
                return Response(serializer.data)
        else:
            return Response({'message': 'Payment cancelled'})
