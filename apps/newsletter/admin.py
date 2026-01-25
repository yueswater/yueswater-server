from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ["email", "nickname", "is_active", "created_at", "unsubscribed_at"]
    list_display_links = ["email", "nickname"]
    search_fields = ["email", "nickname"]
    list_filter = ["is_active", "created_at"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
    actions = ["make_active", "make_inactive"]

    @admin.action(description="標記為訂閱中")
    def make_active(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)

    @admin.action(description="標記為已取消訂閱")
    def make_inactive(self, request, queryset):
        from django.utils import timezone

        queryset.update(is_active=False, unsubscribed_at=timezone.now())
