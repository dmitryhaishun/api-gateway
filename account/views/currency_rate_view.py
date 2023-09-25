from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from account.models import CurrencyRate
from account.serializers.currency_rate_serializer import AllCurrencyRatesSerializer


@extend_schema(
    tags=["Exchange rates"],
)
class CurrencyExchange(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AllCurrencyRatesSerializer
    queryset = CurrencyRate.objects.all()
    parser_classes = [MultiPartParser, FormParser]
