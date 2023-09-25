from rest_framework import serializers


class CardProductsSerializer(serializers.Serializer):
    name = serializers.CharField()
    available_currencies = serializers.ListField(allow_empty=False, max_length=2)
    free_card_servicing = serializers.CharField(allow_blank=True)
    issue_time = serializers.DurationField(max_value="2", min_value="0")
    additional_information = serializers.CharField(allow_blank=True)
    active = serializers.BooleanField()
