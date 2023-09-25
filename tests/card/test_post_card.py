from unittest.mock import patch

import pytest
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

CARDS_URL = reverse("get_cards")
AUTH_TOKEN_URL = reverse("token_obtain_pair")


class TestPostCard:
    @staticmethod
    def test_post_card_no_auth_error(api_client: APIClient):
        response = api_client.post(CARDS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        error_detail = response.data["detail"]
        assert str(error_detail) == "Authentication credentials were not provided."
        assert error_detail.code == "not_authenticated"

    @patch("requests.post")
    @pytest.mark.parametrize(
        "card_data",
        [
            {"card_product_name": "BAD PRODUCT", "currency": "CHF", "payment_system": "VISA"},
            {"card_product_name": "Premium", "currency": "BAD CURRENCY", "payment_system": "VISA"},
            {"card_product_name": "Premium", "currency": "CHF", "payment_system": "BAD System"},
        ],
    )
    def test_post_bad_request(
        self,
        mock_post,
        random_email: str,
        random_password: str,
        user_data: User,
        api_client: APIClient,
        card_data: dict,
    ):
        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        mock_post.return_value = mock_response

        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        response = requests.post(
            f"{CARDS_URL}"
            f"?Branch='-'"
            f"&Card Product={card_data['card_product_name']}"
            f"&Currency={card_data['currency']}"
            f"&Payment System={card_data['payment_system']}"
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch("requests.post")
    def test_post_success(
        self, mock_post, random_email: str, random_password: str, user_data: User, api_client: APIClient
    ):
        expected_result = {
            "id": 10,
            "card_product_id": 2,
            "number": "1463013541620235",
            "cardholder_name": "PAVEL VAR",
            "status": "ISSUANCE",
            "expiration_date": "2028-07-17",
            "payment_system": "VISA",
            "account_number": "00848503179205519007672404",
            "cvv": "602",
            "cash_withdraw_limit": None,
            "card_to_card_limit": None,
            "expenses_limit": None,
            "block_reason": None,
            "created_at": "2023-07-17",
            "issue_term": "2023-07-18",
            "pin": "8966",
        }

        mock_response = requests.Response()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json = lambda: expected_result
        mock_post.return_value = mock_response

        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        data = {
            "address": "Berlin, Bd de Dixmude 40",
            "card_product_name": "Premium",
            "currency": "CHF",
            "payment_system": "VISA",
        }

        response = requests.post(
            f"{CARDS_URL}"
            f"?Branch='-'"
            f"&Card Product={data['card_product_name']}"
            f"&Currency={data['currency']}"
            f"&Payment System={data['payment_system']}"
        )

        result = response.json()
        assert response.status_code == status.HTTP_200_OK
        necessary_fields = (
            "id",
            "card_product_id",
            "number",
            "cardholder_name",
            "status",
            "expiration_date",
            "payment_system",
            "account_number",
            "cvv",
            "cash_withdraw_limit",
            "card_to_card_limit",
            "expenses_limit",
            "block_reason",
            "created_at",
            "issue_term",
            "pin",
        )
        for field in necessary_fields:
            assert field in result
        assert result["card_product_id"] == 2
        assert result["payment_system"] == "VISA"
