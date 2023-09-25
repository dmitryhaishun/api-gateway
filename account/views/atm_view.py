from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from account.models import ATM
from account.serializers.atm_serializer import AllATMSerializer, ATMCitySerializer


class AtmFilter(filters.FilterSet):
    class Meta:
        model = ATM
        fields = ["city"]


@extend_schema(
    tags=["ATM"],
)
class AtmsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ATM.objects.all()
    serializer_class = AllATMSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AtmFilter


@extend_schema(
    tags=["ATM"],
)
class AtmsCity(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ATMCitySerializer
    queryset = ATM.objects.order_by("city").distinct("city")
