from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

GET_ACCOUNT_BY_ID_URL = reverse("account-id", kwargs={"account_id": 1})
GET_ACCOUNT_BY_NUMBER_URL = reverse("account-number", kwargs={"account_number": "1234567890123450"})
AUTH_TOKEN_URL = reverse("token_obtain_pair")


class TestAccounts:
    @patch("requests.get")
    @pytest.mark.parametrize("parameter", ["account_id", "account_number"])
    def test_get_account_by(
        self,
        mock_get,
        api_client: APIClient,
        mock_account_data,
        random_email: str,
        random_password: str,
        user_data: User,
        parameter: str,
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        # Mocked response data
        mocked_response = mock_account_data
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        url = GET_ACCOUNT_BY_ID_URL if parameter == "account_id" else GET_ACCOUNT_BY_NUMBER_URL  # noqa
        response = api_client.get(GET_ACCOUNT_BY_ID_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == mocked_response
