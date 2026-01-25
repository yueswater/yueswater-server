from django.contrib import admin
from django.db import models
from simplemde.widgets import SimpleMDEEditor
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import Category, Post, PostImage, Tag


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    # 列表顯示
    list_display = (
        "title",
        "author",
        "status_badge",
        "created_at",
        "is_draft",
        "is_published",
        "is_archived",
        "get_view_count",
        "get_like_count",
        "category",
    )
    # 進入編輯
    list_display_links = ("title",)
    # 搜尋
    search_fields = ("title", "content", "slug")
    # 過濾器
    list_filter = ("is_published", "is_archived", "created_at", "category")
    # 自動填入 Slug
    prepopulated_fields = {"slug": ("title",)}
    # 唯讀欄位
    readonly_fields = [
        "uuid",
        "created_at",
        "updated_at",
        "get_view_count",
        "get_like_count",
    ]
    # 使用 SimpleMDE 編輯器
    formfield_overrides = {
        models.TextField: {"widget": SimpleMDEEditor},
    }

    class Media:
        css = {"all": ("css/admin_fix.css",)}

    # 顯示狀態
    @display(description="狀態", label=True)
    def status_badge(self, obj):
        if obj.is_archived:
            return "已歸檔", "warning"
        if obj.is_published:
            return "已發布", "success"
        return "草稿", "info"

    # 瀏覽次數
    @display(description="瀏覽次數")
    def get_view_count(self, obj):
        return obj.views.count()

    # 按讚次數
    @display(description="按讚次數")
    def get_like_count(self, obj):
        return obj.likes.count()


@admin.register(PostImage)
class PostImageAdmin(ModelAdmin):
    list_display = ["uuid", "post", "created_at", "image"]
    list_filter = ["created_at"]
    search_fields = ["post__title", "uuid"]
