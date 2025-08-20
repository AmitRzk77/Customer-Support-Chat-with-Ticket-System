from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "is_online", "avatar"]
        read_only_fields = ["id", "role", "is_online"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role"]
        extra_kwargs = { "role": {"required": False} }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", User.Roles.CUSTOMER)
        user = User(**validated_data, role=role)
        user.set_password(self.validated_data["password"])
        user.save()
        return user

class UpdateMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "avatar"]
