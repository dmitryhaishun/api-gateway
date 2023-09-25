from rest_framework import serializers
from loan.helpers.utils import choose_currency


class LoanCreateIncomingSerializer(serializers.Serializer):
    loan_type_id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
    loan_term = serializers.IntegerField(required=True)
    currency = serializers.ChoiceField(choices=choose_currency(), required=True)
    loan_guarantors = serializers.CharField(required=False)
    apr = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
