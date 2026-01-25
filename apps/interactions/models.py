import uuid

from django.conf import settings
from django.db import models
from posts.models import Post


class PostLike(models.Model):
    # 按讚 UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 按讚資訊
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="按讚者",
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="按讚文章",
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP 位址", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="按讚時間")

    class Meta:
        db_table = "post_likes"
        verbose_name = "文章按讚"
        verbose_name_plural = "文章按讚列表"
        unique_together = ("post", "user")
        ordering = ["-created_at"]
        constraints = [
            # 登入使用者：每個文章只能按一次
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_like",
                condition=models.Q(user__isnull=False),
            ),
            # 匿名使用者：每個 IP 對每個文章只能按一次
            models.UniqueConstraint(
                fields=["ip_address", "post"],
                name="unique_ip_like",
                condition=models.Q(user__isnull=True),
            ),
        ]

    def __str__(self):
        return f"{self.user.username} 點了 {self.post.title[:10]} 讚"


class PostView(models.Model):
    # 瀏覽 UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 瀏覽資訊
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="views",
        verbose_name="瀏覽文章",
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP 位址", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="瀏覽時間")

    class Meta:
        db_table = "post_views"
        verbose_name = "文章瀏覽"
        verbose_name_plural = "文章瀏覽列表"
        unique_together = ("post", "ip_address")  # 每個 IP 每篇文章只算一次
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ip_address} 瀏覽了 {self.post.title[:10]}"


class PostComment(models.Model):
    # 留言 UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 留言資訊
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="留言者",
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="留言文章"
    )
    content = models.TextField(verbose_name="留言內容")
    ip_address = models.GenericIPAddressField(
        verbose_name="IP 位址", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="留言時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        db_table = "post_comments"
        verbose_name = "文章留言"
        verbose_name_plural = "文章留言列表"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} 在 {self.post.title[:10]} 上留言"
