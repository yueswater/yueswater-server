import logging

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from interactions.models import PostLike, PostView
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from utils.pdf_handler import convert_post_to_pdf

from .models import Category, Post, PostImage, Tag
from .serializers import (
    CategorySerializer,
    PostImageSerializer,
    PostSerializer,
    TagSerializer,
)

logger = logging.getLogger("apps")


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def like(self, request, slug=None):
        post = self.get_object()
        user = request.user

        like_obj, created = PostLike.objects.get_or_create(user=user, post=post)

        if not created:
            like_obj.delete()
            return Response({"status": "unliked"})

        return Response({"status": "liked"})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def view(self, request, slug=None):
        """記錄瀏覽"""
        post = self.get_object()
        ip = self.get_client_ip(request)

        PostView.objects.get_or_create(post=post, ip_address=ip)

        return Response({"status": "viewed"})


class PostPDFDownloadView(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            post = get_object_or_404(Post, slug=slug)
            pdf_content = convert_post_to_pdf(post)
            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{post.slug}.pdf"'
            return response
        except Exception as e:
            return HttpResponse(str(e), status=500)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(count=Count("posts")).order_by("-count")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.annotate(count=Count("posts")).order_by("-count")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all().order_by("-created_at")
    serializer_class = PostImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):

        slug = serializer.validated_data.get("slug")

        logger.info(
            f"Image Uploading... User: {self.request.user}, Slug provided: {slug}"
        )

        post = None
        if slug:
            post = Post.objects.filter(slug=slug).first()
            if not post:
                logger.warning(
                    f"Image Upload: Slug '{slug}' found but no matching Post."
                )

        serializer.save(post=post)
