from django.urls import path
from .views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='RegisterView'),
    path('login/', TokenObtainPairView.as_view(), name='tokenObtain'),
    path('api/login-refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
]
