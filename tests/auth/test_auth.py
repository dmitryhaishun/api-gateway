from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.auth.test_registration import GET_USERS_URL

AUTH_TOKEN_URL = reverse("token_obtain_pair")
AUTH_REFRESH_TOKEN_URL = reverse("token_refresh")


class TestAuthUser:
    def test_validate_with_valid_email(
        self, user_data: dict, api_client: APIClient, random_email: str, random_password: str
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

    def test_validate_with_email_missing_at_symbol(self, user_data: dict, api_client: APIClient, random_password: str):
        response = api_client.post(AUTH_TOKEN_URL, {"email": "invalidemail.com", "password": random_password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_with_email_missing_dot_symbol(self, user_data: dict, api_client: APIClient, random_password: str):
        response = api_client.post(AUTH_TOKEN_URL, {"email": "invalid.email@com", "password": random_password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_with_nonexistent_email(self, user_data: dict, api_client: APIClient, random_password: str):
        non_existent_email = "nonexistent@example.com"
        response = api_client.post(AUTH_TOKEN_URL, {"email": non_existent_email, "password": random_password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_with_wrong_password(self, user_data: dict, api_client: APIClient, random_email: str):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": "wrongpassword"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRefreshToken:
    def test_valid_refresh_token(self, user_data: dict, api_client: APIClient, random_email: str, random_password: str):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        valid_auth_response = api_client.post(AUTH_REFRESH_TOKEN_URL, {"refresh": response.json()["refresh"]})
        assert valid_auth_response.status_code == status.HTTP_200_OK

    def test_invalid_refresh_token(
        self, user_data: dict, api_client: APIClient, random_email: str, random_password: str
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        invalid_auth_response = api_client.post(AUTH_REFRESH_TOKEN_URL, {"refresh": response.json()["refresh"] + "1"})
        assert invalid_auth_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert invalid_auth_response.json()["detail"] == "Token is invalid or expired"

    def test_adding_refresh_token_to_blacklist(
        self, user_data: dict, api_client: APIClient, random_email: str, random_password: str
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        response_refresh = api_client.post(AUTH_REFRESH_TOKEN_URL, {"refresh": response.json()["refresh"]})
        assert response_refresh.status_code == status.HTTP_200_OK
        response_refresh_again = api_client.post(AUTH_REFRESH_TOKEN_URL, {"refresh": response.json()["refresh"]})
        assert response_refresh_again.status_code == status.HTTP_401_UNAUTHORIZED


class TestEndpointWithAuthPermission:
    def test_view_valid_access_token(
        self, user_data: dict, api_client: APIClient, random_email: str, random_password: str
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        token = response.json()["access"]
        valid_auth_response = api_client.options(GET_USERS_URL, headers={"Authorization": f"JWT {token}"})
        assert valid_auth_response.status_code == status.HTTP_200_OK

    def test_view_invalid_access_token(
        self, user_data: dict, api_client: APIClient, random_email: str, random_password: str
    ):
        response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        token = response.json()["access"]
        valid_auth_response = api_client.options(GET_USERS_URL, headers={"Authorization": f"JWT {token}" + "a"})
        assert valid_auth_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_access_token(user_data: dict, api_client: APIClient, random_email: str, random_password: str):
    response = api_client.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
    access_token = response.json()["access"]
    refresh_token = response.json()["refresh"]

    response_refresh = api_client.post(AUTH_REFRESH_TOKEN_URL, {"refresh": refresh_token})
    new_access_token = response_refresh.json()["access"]
    assert access_token != new_access_token

    valid_auth_response = api_client.options(GET_USERS_URL, headers={"Authorization": f"JWT {new_access_token}"})
    assert valid_auth_response.status_code == status.HTTP_200_OK
