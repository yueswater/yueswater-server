import uuid
from django.utils import timezone
from django.conf import settings
from django.db import models

from utils.image_handler import post_image_upload_path


class Category(models.Model):
    # 分類 UUID
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="分類 UUID"
    )
    # 分類資訊
    name = models.CharField(max_length=100, unique=True, verbose_name="分類名稱")
    description = models.TextField(blank=True, null=True, verbose_name="分類描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        db_table = "categories"
        verbose_name = "文章分類"
        verbose_name_plural = "文章分類列表"

    def __str__(self):
        return self.name


class Tag(models.Model):
    # 標籤 UUID
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="標籤 UUID"
    )
    # 標籤資訊
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤名稱")
    description = models.TextField(blank=True, null=True, verbose_name="標籤描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        db_table = "tags"
        verbose_name = "文章標籤"
        verbose_name_plural = "文章標籤列表"

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章 UUID
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="文章 UUID"
    )
    # 文章資訊
    title = models.CharField(max_length=200, verbose_name="文章標題")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="文章別名")
    content = models.TextField(verbose_name="文章內容")
    excerpt = models.TextField(blank=True, null=True, verbose_name="文章摘要")
    cover_image = models.ImageField(
        upload_to="covers/", blank=True, null=True, help_text="文章縮圖"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="發布時間")

    # 文章狀態
    is_draft = models.BooleanField(default=True, verbose_name="是否為草稿")
    is_archived = models.BooleanField(default=False, verbose_name="是否封存")
    is_published = models.BooleanField(default=False, verbose_name="是否發布")

    # 作者關聯
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="作者",
    )

    # 文章關聯
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="分類",
    )

    # 標籤關聯
    tags = models.ManyToManyField(Tag, related_name="posts", verbose_name="標籤")

    class Meta:
        db_table = "posts"
        ordering = ["-published_at", "-updated_at", "-created_at", "title"]
        verbose_name = "文章"
        verbose_name_plural = "文章列表"

    def __str__(self):
        return self.title

    @property
    def view_count(self):
        return self.views.count()


class PostImage(models.Model):
    # UUID
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="圖片 UUID"
    )
    # 關聯文章
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="所屬文章",
        null=True,
        blank=True,
    )
    # 圖片檔案
    image = models.ImageField(upload_to=post_image_upload_path, verbose_name="圖片檔案")
    # 圖片描述
    alt_text = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="替代文字"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")

    class Meta:
        db_table = "post_images"
        verbose_name = "文章圖片"
        verbose_name_plural = "文章圖片列表"

    def __str__(self):
        return (
            f"Image {self.uuid} for {self.post.title if self.post else 'Unknown Post'}"
        )
