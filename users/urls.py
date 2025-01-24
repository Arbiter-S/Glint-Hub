from django.urls import path
from .views import UserRegisterView, VerifyEmail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='RegisterView'),
    path('login/', TokenObtainPairView.as_view(), name='tokenObtain'),
    path('login-refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
    path('verify-email/', VerifyEmail.as_view(), name='EmailVerification'),
]
