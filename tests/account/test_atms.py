from django.test import Client
from django.urls import reverse
from rest_framework import status

TEST_URL = reverse("atms-list")


class TestAtms:
    def test_atms(self, client: Client, atm_data: dict):
        print(f"{TEST_URL=}")
        response = client.get(TEST_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
