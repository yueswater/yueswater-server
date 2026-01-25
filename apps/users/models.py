import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 使用者 UUID
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="使用者 UUID"
    )
    # 個人簡介
    bio = models.TextField(blank=True, null=True, verbose_name="個人簡介")
    # 大頭貼圖片
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="大頭貼圖片"
    )
    # 最後登出時間
    last_logout = models.DateTimeField(
        blank=True, null=True, verbose_name="最後登出時間"
    )

    class Meta:
        db_table = "users"
        verbose_name = "使用者"
        verbose_name_plural = "使用者列表"

    def __str__(self):
        return self.username

    def unfold_avatar(self):
        """回傳大頭貼圖片的 URL"""
        if self.avatar:
            return self.avatar.url
        return None
