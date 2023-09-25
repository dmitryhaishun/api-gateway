from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.Serializer):
    message = serializers.CharField()


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class AllUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
