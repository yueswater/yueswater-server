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
    list_display = (
        "title",
        "author",
        "status_badge",
        "created_at",
        "updated_at",
        "is_draft",
        "is_published",
        "is_archived",
        "get_view_count",
        "get_like_count",
        "category",
    )
    list_display_links = ("title",)
    search_fields = ("title", "content", "slug")
    list_filter = ("is_published", "is_archived", "created_at", "category")
    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = [
        "uuid",
        "updated_at",
        "get_view_count",
        "get_like_count",
    ]

    fields = (
        "title",
        "slug",
        "author",
        "category",
        "tags",
        "cover_image",
        "content",
        "excerpt",
        "created_at",
        "updated_at",
        "is_published",
        "is_archived",
        "uuid",
    )

    formfield_overrides = {
        models.TextField: {"widget": SimpleMDEEditor},
    }

    class Media:
        css = {"all": ("css/admin_fix.css",)}

    @display(description="狀態", label=True)
    def status_badge(self, obj):
        if obj.is_archived:
            return "已歸檔", "warning"
        if obj.is_published:
            return "已發布", "success"
        return "草稿", "info"

    @display(description="瀏覽次數")
    def get_view_count(self, obj):
        return obj.views.count()

    @display(description="按讚次數")
    def get_like_count(self, obj):
        return obj.likes.count()


@admin.register(PostImage)
class PostImageAdmin(ModelAdmin):
    list_display = ["uuid", "post", "created_at", "image"]
    list_filter = ["created_at"]
    search_fields = ["post__title", "uuid"]
