from rest_framework import status
from rest_framework.response import Response

from account.helpers.enums import AccountType, Currency
from account.models import CurrencyRate
from auth_user.serializers.notification_serializer import ErrorSerializer


def choose_currency() -> list:
    return [currency.value for currency in Currency]


def choose_account_type() -> list:
    return [type.value for type in AccountType]


def parse_error_422(response) -> Response:
    return Response(
        ErrorSerializer(
            {"error": f'{response.json()["detail"][0]["loc"][1]}: {response.json()["detail"][0]["msg"]}'}
        ).data,
        status=status.HTTP_400_BAD_REQUEST,
    )


def get_rates() -> dict:
    return {
        currency.currency: {"buy": str(currency.buy), "sell": str(currency.sell)}
        for currency in CurrencyRate.objects.all()
    }
