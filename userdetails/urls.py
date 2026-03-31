from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,SendOTPView, VerifyOTPView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users'),

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("password-reset/send-otp/", SendOTPView.as_view()),
    path("password-reset/verify-otp/", VerifyOTPView.as_view())
]
