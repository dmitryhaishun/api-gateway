from unittest import mock
from unittest.mock import patch

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

GET_CARDS_URL = reverse("get_cards")
GET_CARD_BY_ID_URL = reverse("crud_card", kwargs={"id": 1})
AUTH_TOKEN_URL = reverse("token_obtain_pair")


class TestCards:
    @patch("requests.post")
    def test_get_all_cards(
        self,
        mock_post,
        api_client: APIClient,
        mock_data_cards,
        random_email: str,
        random_password: str,
        user_data: User,
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        # Mocked response data
        mocked_response = mock_data_cards
        mock_post.return_value.json.return_value = mocked_response
        mock_post.return_value.status_code = status.HTTP_200_OK
        response = api_client.post(GET_CARDS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == mocked_response

    @patch("requests.get")
    def test_get_card_by_id(
        self,
        mock_get,
        api_client: APIClient,
        mock_data_for_card,
        random_email: str,
        random_password: str,
        user_data: User,
    ):
        data = mock_data_for_card["user_uuid"]  # noqa
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        # Mocked response data
        mocked_response = mock_data_for_card
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_CARD_BY_ID_URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestCardError:
    def test_get_all_cards_error(self, api_client, random_email: str, random_password: str, user_data: User):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        with mock.patch("requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.RequestException

            response = api_client.get(GET_CARDS_URL)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_card_by_id_error(
        self, api_client: APIClient, mock_data_for_card, random_email: str, random_password: str, user_data: User
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        with mock.patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException

            response = api_client.get(GET_CARD_BY_ID_URL)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
