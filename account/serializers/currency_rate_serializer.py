from rest_framework import serializers

from account.models import CurrencyRate


class AllCurrencyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = "__all__"
