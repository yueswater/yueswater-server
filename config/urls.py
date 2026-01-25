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
    TokenRefreshView,
)
from users.views import (
    ActivateAccountView,
    CustomTokenObtainPairView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    UserProfileView,
    ChangePasswordView,
)

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
    path(
        "api/auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("api/auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/auth/verify-email/",
        ActivateAccountView.as_view(),
        name="auth_verify_email",
    ),
    path(
        "api/auth/password-reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "api/auth/password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/auth/change-password/", ChangePasswordView.as_view(), name="auth_change_password"),
]

# 圖片與靜態檔案設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
