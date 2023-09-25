from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    message = serializers.CharField()
