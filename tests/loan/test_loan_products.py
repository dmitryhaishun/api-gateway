from unittest import mock
from unittest.mock import patch

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

AUTH_TOKEN_URL = reverse("token_obtain_pair")
GET_LOAN_PRODUCT_URL = reverse("get_loan_products")
GET_ONE_LOAN_PRODUCT_URL = reverse("get_loan_product_by_id", kwargs={"loan_product_id": 2})
GET_ONE_LOAN_PRODUCT_FAIL_URL = reverse("get_loan_product_by_id", kwargs={"loan_product_id": 20})


class TestGetLoanProduct:
    @patch("requests.get")
    def test_get_loan_product_success(
        self,
        mock_get,
        mock_loan_products,
        api_client: APIClient,
    ):
        mocked_response = mock_loan_products
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_LOAN_PRODUCT_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    @patch("requests.get")
    def test_get_loan_product_by_id_success(
        self,
        mock_get,
        mock_loan_products,
        api_client: APIClient,
    ):
        mocked_response = mock_loan_products[1]
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_ONE_LOAN_PRODUCT_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    @patch("requests.get")
    def test_get_loan_product_by_id_fail(
        self,
        mock_get,
        api_client: APIClient,
    ):
        mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        mock_get.return_value.json.return_value = {"detail": "Loan product not found"}

        response = api_client.get(GET_ONE_LOAN_PRODUCT_FAIL_URL)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Loan product not found"

    def test_get_loan_products_error(self, api_client: APIClient):
        with mock.patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            response = api_client.get(GET_LOAN_PRODUCT_URL)
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
