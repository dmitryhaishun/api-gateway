from django.test import Client
from rest_framework import status


def test_api_gateway(client: Client):
    response = client.get("/api/user/")
    assert response.status_code == status.HTTP_200_OK
