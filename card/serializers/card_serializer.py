from rest_framework import serializers

from card.helpers.enums import BlockReason, CardStatus


class CardPatchStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[(member.value, member.name) for member in CardStatus])
    block_reason = serializers.ChoiceField(
        choices=[(member.value, member.name) for member in BlockReason], allow_null=True
    )


class AllCardSerializer(CardPatchStatusSerializer):
    id = serializers.IntegerField()
    card_product_id = serializers.IntegerField()
    number = serializers.CharField()
    cardholder_name = serializers.CharField()
    expiration_date = serializers.DateField()
    payment_system = serializers.CharField()
    account_number = serializers.CharField()
    cvv = serializers.CharField(min_length=3, max_length=3)
    cash_withdraw_limit = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True)
    card_to_card_limit = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True)
    expenses_limit = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True)
    created_at = serializers.DateTimeField()
    issue_term = serializers.DateTimeField()
    pin = serializers.CharField(min_length=4, max_length=4)


class CardLimitsSerializer(serializers.Serializer):
    cash_withdraw_limit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    card_to_card_limit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    expenses_limit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
