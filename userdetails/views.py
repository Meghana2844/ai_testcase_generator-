from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
       
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
       
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import PasswordResetOTP
from .utils import generate_otp
from .serializers import SendOTPSerializer, VerifyOTPSerializer

user = get_user_model()

class SendOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email).first()

        # Do not reveal if user exists
        if user:
            # Delete old OTPs
            PasswordResetOTP.objects.filter(user=user).delete()

            otp = generate_otp()

            PasswordResetOTP.objects.create(user=user, otp=otp)

            send_mail(
                "Password Reset OTP",
                f"Your OTP is {otp}",
                "noreply@yourapp.com",
                [email],
            )

        return Response({"message": "If email exists, OTP sent"})


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Invalid request"}, status=400)

        record = PasswordResetOTP.objects.filter(
            user=user, otp=otp, is_used=False
        ).last()

        if not record:
            return Response({"error": "Invalid OTP"}, status=400)

        if record.is_expired():
            return Response({"error": "OTP expired"}, status=400)

        # Mark OTP as used
        record.is_used = True
        record.save()

        # Reset password
        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})