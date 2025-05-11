from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    VerifyEmailView,
    UserViewSet,
    ForgotPasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ValidateResetTokenView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('validate-reset-token/<str:token>/', ValidateResetTokenView.as_view(), name='validate-reset-token'),
]
