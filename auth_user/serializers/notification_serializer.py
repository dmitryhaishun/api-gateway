from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class OtpErrorSerializer(serializers.Serializer):
    otp_code = serializers.ListField()


class EmailErrorSerializer(serializers.Serializer):
    email = serializers.CharField()
