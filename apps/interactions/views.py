from django.db.models import Q
from posts.models import Post
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.network import get_client_ip

from .models import PostBookmark, PostComment, PostLike
from .serializers import BookmarkSerializer, CommentSerializer, LikeSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class CommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.select_related("user", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        post_slug = self.request.query_params.get("post_slug")
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        return queryset


class LikeViewSet(viewsets.GenericViewSet):
    queryset = PostLike.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        post_id = request.data.get("post")
        if not post_id:
            return Response(
                {"error": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        ip = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # 查詢是否已經按讚
        if user:
            like_query = PostLike.objects.filter(post=post, user=user)
        else:
            like_query = PostLike.objects.filter(
                post=post, ip_address=ip, user__isnull=True
            )

        if like_query.exists():
            # 已按讚 -> 取消按讚
            like_query.delete()
            liked = False
        else:
            # 未按讚 -> 新增按讚
            PostLike.objects.create(
                post=post, user=user, ip_address=ip if not user else None
            )
            liked = True

        # 回傳最新的按讚數與狀態
        return Response({"liked": liked, "likes_count": post.likes.count()})

    @action(detail=False, methods=["get"])
    def status(self, request):
        post_id = request.query_params.get("post_id")
        if not post_id:
            return Response(
                {"error": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        ip = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # 查詢是否按讚
        if user:
            is_liked = PostLike.objects.filter(post=post, user=user).exists()
        else:
            is_liked = PostLike.objects.filter(
                post=post, ip_address=ip, user__isnull=True
            ).exists()

        return Response({"liked": is_liked, "likes_count": post.likes.count()})


class BookmarkViewSet(viewsets.GenericViewSet):
    queryset = PostBookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        post_id = request.data.get("post")
        if not post_id:
            return Response(
                {"error": "文章 ID 是必填項"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        bookmark_query = PostBookmark.objects.filter(post=post, user=user)

        if bookmark_query.exists():
            bookmark_query.delete()
            bookmarked = False
        else:
            PostBookmark.objects.create(post=post, user=user)
            bookmarked = True

        return Response({"bookmarked": bookmarked})

    @action(detail=False, methods=["get"])
    def status(self, request):
        post_id = request.query_params.get("post_id")
        if not post_id:
            return Response(
                {"error": "文章 ID 是必填項"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND)

        is_bookmarked = PostBookmark.objects.filter(
            post=post, user=request.user
        ).exists()
        return Response({"bookmarked": is_bookmarked})

    @action(detail=False, methods=["get"])
    def my_list(self, request):
        bookmarks = (
            PostBookmark.objects.filter(user=request.user)
            .select_related("post", "post__category")
            .prefetch_related("post__tags")
        )

        data = []
        for b in bookmarks:
            data.append(
                {
                    "id": b.id,
                    "title": b.post.title,
                    "slug": b.post.slug,
                    "created_at": b.created_at,
                    "post": {
                        "category": {
                            "name": (
                                b.post.category.name if b.post.category else "未分類"
                            )
                        },
                        "tags": [{"name": t.name} for t in b.post.tags.all()],
                    },
                }
            )
        return Response(data)
