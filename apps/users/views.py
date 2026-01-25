import logging
import smtplib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        self.send_verification_email(user)

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = (
            f"https://www.yueswater.com/verify-email?uid={uid}&token={token}"
        )

        subject = "【岳氏礦泉水】請驗證您的電子郵件"
        context = {
            "username": user.username,
            "verification_link": verification_link,
            "current_year": timezone.now().year,
        }

        try:
            print(f"DEBUG: STARTing email process for {user.email}")
            html_content = render_to_string("users/verification_email.html", context)
            text_content = strip_tags(html_content)
            print("DEBUG: Template rendered")

            connection = get_connection(fail_silently=False)
            connection.open()
            print("DEBUG: SMTP Connection opened")

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                connection=connection,
            )
            msg.attach_alternative(html_content, "text/html")

            print("DEBUG: Attempting msg.send()...")
            msg.send(fail_silently=False)
            print(f"DEBUG: SUCCESS - Sent to {user.email}")
            connection.close()

        except smtplib.SMTPException as e:
            print(f"DEBUG: SMTP ERROR - {str(e)}")
        except Exception as e:
            print(f"DEBUG: GENERAL ERROR - {type(e).__name__}: {str(e)}")


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            if user.is_active:
                return Response(
                    {"detail": "already_active"}, status=status.HTTP_200_OK
                )
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {"detail": "activated"}, status=status.HTTP_200_OK
                )
                
        return Response(
            {"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.last_logout = timezone.now()
            user.save()
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
