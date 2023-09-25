from rest_framework import serializers

from account.models import ATM


class AllATMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATM
        fields = "__all__"


class ATMCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ATM
        fields = ["id", "city"]
