from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

AUTH_TOKEN_URL = reverse("token_obtain_pair")


class TestUserInfo:
    USER_INFO_URL = "/api/user/info/"
    CLIENT = APIClient()

    def test_get_user_info_by_unauthorized_user(self):
        response = self.CLIENT.get(self.USER_INFO_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_info_by_authorized_user(self, random_email: str, random_password: str, user_data: User):
        response = self.CLIENT.post(AUTH_TOKEN_URL, {"email": random_email, "password": random_password})
        assert response.status_code == status.HTTP_200_OK

        access_token = response.data.get("access")

        self.CLIENT.force_authenticate(user=user_data, token=access_token)

        response = self.CLIENT.get(self.USER_INFO_URL)
        assert response.status_code == status.HTTP_200_OK

        assert len(response.data) != 1, f"More than 1 authorized user: {len(response.data)}"

        necessary_fields = ("email", "first_name", "last_name")
        result = response.data
        for field in necessary_fields:
            assert field in result

        assert result["email"] == user_data.email
        assert result["first_name"] == user_data.first_name
        assert result["last_name"] == user_data.last_name
