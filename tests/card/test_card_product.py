from unittest import mock
from unittest.mock import patch

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

AUTH_TOKEN_URL = reverse("token_obtain_pair")
GET_CARD_PRODUCT_URL = reverse("get_card_products")


class TestGetCardProduct:
    @patch("requests.get")
    def test_get_card_product_success(
        self,
        mock_get,
        api_client: APIClient,
        mock_data_card_products,
        random_email: str,
        random_password: str,
        user_data: User,
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        mocked_response = mock_data_card_products
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_CARD_PRODUCT_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == mocked_response

    def test_get_card_products_error(
        self, api_client: APIClient, random_email: str, random_password: str, user_data: User
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        with mock.patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            response = api_client.get(GET_CARD_PRODUCT_URL)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
