from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "bio")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
        )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "avatar",
            "date_joined",
            "is_active",
        )

    def get_avatar(self, obj):
        if not obj.avatar:
            return None
        return obj.avatar.url


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    客製化 JWT 登入回傳內容，加入使用者資訊與 Avatar
    """

    def validate(self, attrs):

        data = super().validate(attrs)

        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["email"] = self.user.email

        if self.user.avatar:

            request = self.context.get("request")
            if request:
                data["avatar"] = request.build_absolute_uri(self.user.avatar.url)
            else:
                data["avatar"] = self.user.avatar.url
        else:
            data["avatar"] = None

        return data
