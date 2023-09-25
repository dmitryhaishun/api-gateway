from rest_framework import serializers


class TransactionRequestSerializer(serializers.Serializer):
    write_off_account = serializers.CharField(min_length=16, max_length=16, default="5728393862235074")
    crediting_account = serializers.CharField(min_length=16, max_length=16, default="2554542495491224")
    transaction_sum = serializers.DecimalField(max_digits=10, decimal_places=2, default=10, min_value=1)
    save_transaction = serializers.BooleanField(default=False)
    transaction_type = serializers.CharField(default="Between my accounts")
    transaction_title = serializers.CharField(default="Favorite transaction")

    @staticmethod
    def validate_write_off_account(value) -> str:
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Write_off_account must be a 16-digit number")
        return value

    @staticmethod
    def validate_crediting_account(value) -> str:
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Crediting_account must be a 16-digit number")
        return value


class CardTransactionRequestSerializer(serializers.Serializer):
    write_off_card = serializers.CharField(min_length=16, max_length=16, default="5728393862235074")
    crediting_card = serializers.CharField(min_length=16, max_length=16, default="2554542495491224")
    transaction_sum = serializers.DecimalField(max_digits=10, decimal_places=2, default=10, min_value=1)
    save_transaction = serializers.BooleanField(default=False)
    transaction_type = serializers.CharField(default="Cards transfers")
    transaction_title = serializers.CharField(default="Favorite transaction", allow_null=True)

    @staticmethod
    def validate_write_off_account(value) -> str:
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Write_off_card must be a 16-digit number")
        return value

    @staticmethod
    def validate_crediting_account(value) -> str:
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Crediting_card must be a 16-digit number")
        return value


class SuccessSerializer(serializers.Serializer):
    message = serializers.CharField(default="Success operation")
