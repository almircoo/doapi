import uuid
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile, PasswordReset
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    ProfileSerializer,
    RegisterSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from common.utils import send_email

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that uses our enhanced serializer."""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """API view for user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate verification token
        token = str(uuid.uuid4())
        user.email_verification_token = token
        user.save()
        
        # Send verification email
        context = {
            'user': user,
            'verification_url': f"{request.build_absolute_uri('/').rstrip('/')}/api/verify-email/{token}/",
        }
        send_email(
            to_email=user.email,
            subject="Verify your email address",
            template_name="accounts/email_verification.html",
            context=context
        )
        
        return Response(
            {"message": "User registered successfully. Please check your email to verify your account."},
            status=status.HTTP_201_CREATED
        )


class VerifyEmailView(generics.GenericAPIView):
    """API view for email verification."""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid verification token."}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        # Users can only see their own profile
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get the current user's profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update the current user's profile."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change the current user's password."""
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check current password
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"message": "Password updated successfully."})


class ForgotPasswordView(generics.GenericAPIView):
    """API view for initiating the forgot password process."""
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = str(uuid.uuid4())
            expires_at = timezone.now() + timedelta(hours=24)
            
            # Save reset token
            PasswordReset.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # Send reset email
            frontend_url = request.data.get('frontend_url', 'http://localhost:3000')
            reset_url = f"{frontend_url}/reset-password/{token}"
            
            context = {
                'user': user,
                'reset_url': reset_url,
                'expires_in': '24 hours',
            }
            
            send_email(
                to_email=user.email,
                subject="Reset your password",
                template_name="accounts/password_reset.html",
                context=context
            )
            
            return Response(
                {"message": "If an account with that email exists, we've sent password reset instructions."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist for security reasons
            return Response(
                {"message": "If an account with that email exists, we've sent password reset instructions."},
                status=status.HTTP_200_OK
            )


class PasswordResetRequestView(generics.GenericAPIView):
    """API view for requesting a password reset."""
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = str(uuid.uuid4())
            expires_at = timezone.now() + timedelta(hours=24)
            
            # Save reset token
            PasswordReset.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # Send reset email
            context = {
                'user': user,
                'reset_url': f"{request.build_absolute_uri('/').rstrip('/')}/reset-password/{token}/",
                'expires_in': '24 hours',
            }
            send_email(
                to_email=user.email,
                subject="Reset your password",
                template_name="accounts/password_reset.html",
                context=context
            )
            
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """API view for confirming a password reset."""
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_password = serializer.validated_data['new_password']
        
        try:
            # Find valid reset token
            reset = PasswordReset.objects.get(
                token=token,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            
            # Reset the password
            user = reset.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset.is_used = True
            reset.save()
            
            # Invalidate all other reset tokens for this user
            PasswordReset.objects.filter(
                user=user,
                is_used=False
            ).update(is_used=True)
            
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except PasswordReset.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class ValidateResetTokenView(generics.GenericAPIView):
    """API view for validating a password reset token."""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            # Check if token exists and is valid
            reset = PasswordReset.objects.get(
                token=token,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except PasswordReset.DoesNotExist:
            return Response({"valid": False}, status=status.HTTP_200_OK)
