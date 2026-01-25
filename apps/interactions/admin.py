from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import PostComment, PostLike


@admin.register(PostLike)
class PostLikeAdmin(ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title")


@admin.register(PostComment)
class PostCommentAdmin(ModelAdmin):
    list_display = ("user", "post", "content_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title", "content")

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "留言預覽"
