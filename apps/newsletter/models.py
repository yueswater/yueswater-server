import uuid

from django.db import models


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="訂閱者暱稱"
    )
    email = models.EmailField(unique=True, verbose_name="訂閱信箱")
    is_active = models.BooleanField(default=True, verbose_name="是否訂閱中")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="訂閱時間")
    unsubscribed_at = models.DateTimeField(
        blank=True, null=True, verbose_name="取消訂閱時間"
    )

    class Meta:
        db_table = "newsletter_subscribers"
        verbose_name = "電子報訂閱者"
        verbose_name_plural = "電子報訂閱列表"
        ordering = ["-created_at"]

    def __str__(self):
        name = self.nickname if self.nickname else self.email
        return f"{name} ({'訂閱中' if self.is_active else '已取消'})"
