from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

AUTH_TOKEN_URL = reverse("token_obtain_pair")
GET_LOANS = reverse("get_loans_or_loan_applications")
GET_LOAN_BY_ID = reverse("get_loan_by_id", kwargs={"loan_id": 1})
CREATE_LOAN_URL = reverse("create_new_loan")


class TestGetLoans:
    @patch("requests.get")
    def test_get_loans(
        self,
        mock_get,
        api_client: APIClient,
        mock_loans_data,
        random_email: str,
        random_password: str,
        user_data: User,
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        mocked_response = mock_loans_data
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_LOANS, data={"loan_type": "loans", "offset": 0, "limit": 100})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @patch("requests.get")
    def test_get_loan_applications(
        self,
        mock_get,
        api_client: APIClient,
        mock_loans_data,
        random_email: str,
        random_password: str,
        user_data: User,
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        mocked_response = mock_loans_data
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_LOANS, data={"loan_type": "applications", "offset": 0, "limit": 100})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @patch("requests.get")
    def test_get_loan_by_id(
        self,
        mock_get,
        api_client: APIClient,
        mock_loans_data,
        random_email: str,
        random_password: str,
        user_data: User,
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        mocked_response = mock_loans_data
        mock_get.return_value.json.return_value = mocked_response
        mock_get.return_value.status_code = status.HTTP_200_OK

        response = api_client.get(GET_LOAN_BY_ID, data={"loan_id": 1})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Loan with id 1 not found"


class TestCreateNewLoanView:
    @patch("requests.post")
    def test_create_new_loan(
        self,
        mock_post,
        api_client: APIClient,
        random_email: str,
        random_password: str,
        user_data: User
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")
        api_client.force_authenticate(user=user_data, token=access_token)

        mock_response_data = {"message": "Loan application has been made"}
        mock_post.return_value.json.return_value = mock_response_data
        mock_post.return_value.status_code = status.HTTP_201_CREATED

        loan_data = {
            "loan_type_id": 1,
            "amount": 10000,
            "loan_term": 31536000,
            "currency": "USD",
            "loan_guarantors": "John Doe",
            "apr": 5.25,
        }

        response = api_client.post(CREATE_LOAN_URL, json=loan_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == mock_response_data
