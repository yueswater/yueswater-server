from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD_SETTINGS = {
    "SITE_TITLE": "岳氏礦泉水",
    "SITE_HEADER": "岳氏礦泉水後台管理",
    "SITE_URL": "/",
    # "SITE_ICON":  lambda request: static("logo.svg"),
    # 功能設定
    "USER_AVATAR": "unfold_avatar",
    # 側邊欄設定
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("主控台"),
                "separator": True,
                "items": [
                    {
                        "title": _("總覽儀表板"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("使用者管理"),
                "separator": True,
                "items": [
                    {
                        "title": _("使用者列表"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("群組權限"),
                        "icon": "lock",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("內容管理"),
                "separator": True,
                "items": [
                    {
                        "title": _("所有文章"),
                        "icon": "article",
                        "link": reverse_lazy("admin:posts_post_changelist"),
                    },
                    {
                        "title": _("文章分類"),
                        "icon": "category",
                        "link": reverse_lazy("admin:posts_category_changelist"),
                    },
                    {
                        "title": _("文章標籤"),
                        "icon": "sell",
                        "link": reverse_lazy("admin:posts_tag_changelist"),
                    },
                ],
            },
            {
                "title": _("互動數據"),
                "separator": True,
                "items": [
                    {
                        "title": _("按讚紀錄"),
                        "icon": "thumb_up",
                        "link": reverse_lazy("admin:interactions_postlike_changelist"),
                    },
                    {
                        "title": _("留言管理"),
                        "icon": "chat",
                        "link": reverse_lazy(
                            "admin:interactions_postcomment_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}
