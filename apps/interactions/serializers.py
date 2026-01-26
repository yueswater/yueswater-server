from better_profanity import profanity
from rest_framework import serializers
from users.serializers import UserSerializer

from utils.badwords_handler import load_bad_words_from_file

from .models import PostBookmark, PostComment, PostLike

CUSTOM_BAD_WORDS = load_bad_words_from_file()


profanity.load_censor_words()
profanity.add_censor_words(CUSTOM_BAD_WORDS)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ["id", "user", "post", "content", "created_at"]
        read_only_fields = ["user", "created_at"]

    def validate_content(self, value):
        cleaned_content = value.strip()

        if not cleaned_content:
            raise serializers.ValidationError("留言內容不能為空。")

        for bad_word in CUSTOM_BAD_WORDS:
            if bad_word in cleaned_content:
                raise serializers.ValidationError(
                    "您的留言包含不適當的詞彙，請修正後再發布。"
                )

        if profanity.contains_profanity(cleaned_content):
            raise serializers.ValidationError(
                "您的留言包含不適當的詞彙，請修正後再發布。"
            )

        return cleaned_content


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["id", "post", "created_at"]
        read_only_fields = ["id", "created_at"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBookmark
        fields = ["id", "post", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        post = attrs["post"]

        if PostBookmark.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("您已經收藏過這篇文章了。")

        return attrs
