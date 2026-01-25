from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from interactions.views import CommentViewSet, LikeViewSet
from newsletter.views import NewsletterViewSet
from posts.views import CategoryViewSet, PostImageViewSet, PostViewSet, TagViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 引入 Views
from users.views import LogoutView, RegisterView, TokenObtainPairView, UserProfileView

# 設定 Router
router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"upload", PostImageViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"tags", TagViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"likes", LikeViewSet)
router.register(r"newsletter", NewsletterViewSet, basename="newsletter")

urlpatterns = [
    path("admin/", admin.site.urls),
    # API 文件
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # API 路由
    path("api/", include(router.urls)),
    # 使用者認證
    path("api/auth/register/", RegisterView.as_view(), name="auth_register"),
    path("api/auth/me/", UserProfileView.as_view(), name="auth_me"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# 圖片與靜態檔案設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
