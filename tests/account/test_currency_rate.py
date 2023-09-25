from django.test import Client
from django.urls import reverse
from rest_framework import status

CURRENCY_RATE = reverse("exchange-rates-list")


def test_currency_rate(client: Client):
    response = client.get(CURRENCY_RATE)
    assert response.status_code == status.HTTP_200_OK
