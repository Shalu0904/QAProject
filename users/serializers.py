from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ["id", "email", "name"]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["name", "email", "new_password", "old_password"]

    def validate(self, attrs):

        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")

        if new_password:
            if not old_password:
                msg = "Old password is required to set a new password."
                raise serializers.ValidationError({"old_password": msg})
            if not self.instance.check_password(old_password):
                raise serializers.ValidationError(
                    {"old_password": "Old password is not correct."}
                )

        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)

        # Handle password change
        new_password = validated_data.get("new_password")
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance
