from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscriber
from .serializers import SubscriberSerializer


class NewsletterViewSet(viewsets.GenericViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def subscribe(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]

        nickname = serializer.validated_data.get("nickname")

        subscriber, created = Subscriber.objects.get_or_create(email=email)

        if not created:
            if subscriber.is_active:
                return Response(
                    {"message": "您已經訂閱過了！"}, status=status.HTTP_200_OK
                )
            else:

                subscriber.is_active = True
                if nickname:
                    subscriber.nickname = nickname
                subscriber.save()
        else:

            if nickname:
                subscriber.nickname = nickname
                subscriber.save()

        self.send_welcome_email(email, subscriber.nickname)

        return Response(
            {"message": "訂閱成功！請查看您的信箱。"}, status=status.HTTP_201_CREATED
        )

    def send_welcome_email(self, email, nickname=None):
        subject = "【岳氏礦泉水】感謝您的訂閱！"

        context = {
            "nickname": nickname or "朋友",
            "blog_url": "http://localhost:3000",
            "current_year": datetime.now().year,
        }

        html_content = render_to_string("newsletter/welcome_email.html", context)

        text_content = strip_tags(html_content)

        try:

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )

            msg.attach_alternative(html_content, "text/html")

            msg.send(fail_silently=False)

        except Exception as e:
            print(f"寄送歡迎信失敗: {e}")
