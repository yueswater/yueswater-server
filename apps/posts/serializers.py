from interactions.serializers import CommentSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from utils.network import get_client_ip

from .models import Category, Post, PostImage, Tag


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "uuid", "name", "description", "count", "created_at"]


class TagSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "uuid", "name", "count", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    # 顯示詳細資料
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # 寫入時用 ID
    category_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        source="category",
    )
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        required=False,
        source="tags",
    )

    # 統計欄位
    view_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def get_view_count(self, obj):
        return obj.views.count()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        if request.user and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        ip = get_client_ip(request)
        return obj.likes.filter(ip_address=ip, user__isnull=True).exists()

    class Meta:
        model = Post
        fields = [
            "id",
            "uuid",
            "title",
            "slug",
            "content",
            "excerpt",
            "cover_image",
            "category",  # 讀取用
            "category_id",  # 寫入用
            "tags",  # 讀取用
            "tags_ids",  # 寫入用
            "view_count",
            "like_count",
            "is_draft",
            "is_published",
            "is_archived",
            "created_at",
            "updated_at",
            "published_at",
            "author",
            "is_liked",
            "comments",
        ]
        read_only_fields = [
            "uuid",
            "created_at",
            "updated_at",
            "author",
            "categories",
            "tags",
            "view_count",
            "like_count",
        ]


class PostImageSerializer(serializers.ModelSerializer):
    # 接收前端傳來的 slug
    slug = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = PostImage
        fields = ["uuid", "image", "alt_text", "slug", "created_at"]
        read_only_fields = ["uuid", "created_at"]

    def create(self, validated_data):
        # 取出 slug
        slug = validated_data.pop("slug", None)

        # 建立實例
        instance = PostImage(**validated_data)

        # 如果有 slug 暫存在 instance 上
        if slug:
            instance.temp_slug = slug

        # 存檔
        instance.save()
        return instance
