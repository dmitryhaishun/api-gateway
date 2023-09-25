from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_uuid = serializers.UUIDField()
    currency = serializers.CharField()
    number = serializers.CharField(min_length=16, max_length=16)
    amount = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True)
    created = serializers.DateTimeField()
    account_type = serializers.CharField()
