from better_profanity import profanity
from rest_framework import serializers
from users.serializers import UserSerializer

from utils.badwords_handler import load_bad_words_from_file

from .models import PostComment, PostLike

# 載入自定義髒話列表
CUSTOM_BAD_WORDS = load_bad_words_from_file()

# 初始化髒話過濾器
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
        # 不能只輸入空白
        if not cleaned_content:
            raise serializers.ValidationError("留言內容不能為空。")

        # 檢查髒話
        for bad_word in CUSTOM_BAD_WORDS:
            if bad_word in cleaned_content:
                raise serializers.ValidationError(
                    "您的留言包含不適當的詞彙，請修正後再發布。"
                )

        # 進行更全面的檢查
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
