from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # 列表顯示欄位
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "last_login",
        "last_logout",
        "display_date_joined",
        "display_avatar",
    )
    # 搜尋欄位
    search_fields = ("username", "email")
    # 側邊過濾器
    list_filter = ("is_staff", "is_active", "date_joined")

    # 顯示圖片
    @display(description="大頭貼")
    def display_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url,
            )
        return "-"

    @display(description="加入時間")
    def display_date_joined(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    # 編輯頁面欄位分組
    fieldsets = BaseUserAdmin.fieldsets + (
        ("額外資訊", {"fields": ("bio", "avatar", "uuid")}),
    )
    readonly_fields = ["uuid"]
