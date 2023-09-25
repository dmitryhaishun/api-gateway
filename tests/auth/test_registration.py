import os

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.celery.tasks import send_confirm_to_email

REGISTRATION_URL = reverse("register-list")
FINAL_REGISTRATION_URL = reverse("final_register-list")

GET_USERS_URL = reverse("example-list")


class TestFinalStepRegistration:
    def test_registration(self, api_client: APIClient, data_for_user: dict):
        response = api_client.post(FINAL_REGISTRATION_URL, data=data_for_user)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["first_name"] == data_for_user["first_name"]
        assert response.json()["phone_number"] == data_for_user["phone_number"]
        assert response.json()["passport_id"] == data_for_user["passport_id"]

    def test_unsuccessful_registration(self, api_client: APIClient, data_for_user: dict):
        data_for_user["email"] = "random_email@mail.com"
        response = api_client.post(FINAL_REGISTRATION_URL, data=data_for_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUserRegistrationValidation:
    @pytest.mark.parametrize(
        "first_name, last_name,  http_status",
        [
            # test invalid first_name
            ("", pytest.lazy_fixture("random_last_name"), status.HTTP_400_BAD_REQUEST),
            ("--", pytest.lazy_fixture("random_last_name"), status.HTTP_400_BAD_REQUEST),
            ("-' ", pytest.lazy_fixture("random_last_name"), status.HTTP_400_BAD_REQUEST),
            ("    ", pytest.lazy_fixture("random_last_name"), status.HTTP_400_BAD_REQUEST),
            ("Grisha228", pytest.lazy_fixture("random_last_name"), status.HTTP_400_BAD_REQUEST),
            ("Gena@", pytest.lazy_fixture("random_last_name"), status.HTTP_400_BAD_REQUEST),
            (
                "Oleggggggggggggggggggggggggggggggggggggggggggggggggggggg",
                pytest.lazy_fixture("random_last_name"),
                status.HTTP_400_BAD_REQUEST,
            ),
            # test invalid last_name
            (pytest.lazy_fixture("random_first_name"), "", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_first_name"), "--", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_first_name"), " --'", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_first_name"), "    ", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_first_name"), "Ivanov14", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_first_name"), "Ivanov!", status.HTTP_400_BAD_REQUEST),
            (
                pytest.lazy_fixture("random_first_name"),
                "Ivanovvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv",
                status.HTTP_400_BAD_REQUEST,
            ),
            # test valid first_name and last_name
            (
                pytest.lazy_fixture("random_first_name"),
                pytest.lazy_fixture("random_last_name"),
                status.HTTP_201_CREATED,
            ),
        ],
    )
    def test_first_and_last_name_validation(
        self, api_client: APIClient, data_for_user: dict, first_name: str, last_name: str, http_status: status
    ):
        data_for_user["first_name"] = first_name
        data_for_user["last_name"] = last_name
        response = api_client.post(FINAL_REGISTRATION_URL, data_for_user)
        assert response.status_code == http_status

    @pytest.mark.parametrize(
        "passport_id, phone_number,  http_status",
        [
            # test invalid passport_number
            ("", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            ("a", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            ("AAAAAAAAA", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            ("1111111111a", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            (
                "ddddddddddddddddddddddddddddddddd",
                pytest.lazy_fixture("random_phone_number"),
                status.HTTP_400_BAD_REQUEST,
            ),
            ("MP6626262@", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            ("MP6626262-", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            ("MP6626262!ddddd", pytest.lazy_fixture("random_phone_number"), status.HTTP_400_BAD_REQUEST),
            # test invalid phone_number
            (pytest.lazy_fixture("random_passport_id"), "375297777777", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_passport_id"), "+375298888888@", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_passport_id"), "-375298888888", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_passport_id"), "+asdada", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_passport_id"), "+37529777777777", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_passport_id"), "", status.HTTP_400_BAD_REQUEST),
            # test valid phone and passport
            (
                pytest.lazy_fixture("random_passport_id"),
                pytest.lazy_fixture("random_phone_number"),
                status.HTTP_201_CREATED,
            ),
        ],
    )
    def test_passport_and_phone_validation(
        self, api_client: APIClient, data_for_user: dict, passport_id: str, phone_number: str, http_status: status
    ):
        data_for_user["passport_id"] = passport_id
        data_for_user["phone_number"] = phone_number
        response = api_client.post(FINAL_REGISTRATION_URL, data_for_user)
        assert response.status_code == http_status

    @pytest.mark.parametrize(
        "email, password,  http_status",
        [
            # test invalid mail
            ("user@mailru", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            ("user-mail.ru", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            ("usermail.r@u", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            ("userm@ail.r", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            ("user228_@mail.ru", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            ("@a.ru", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            (
                "userrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr@email.ru",
                pytest.lazy_fixture("random_password"),
                status.HTTP_400_BAD_REQUEST,
            ),
            ("", pytest.lazy_fixture("random_password"), status.HTTP_400_BAD_REQUEST),
            # test invalid password
            (pytest.lazy_fixture("random_email"), "", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_email"), "Qwe@1", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_email"), "Qwerty12333", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_email"), "werty123333@", status.HTTP_400_BAD_REQUEST),
            (pytest.lazy_fixture("random_email"), "Qwerty@@@@@@@@@", status.HTTP_400_BAD_REQUEST),
            (
                pytest.lazy_fixture("random_email"),
                "qwerty123@dddddddddddddddddddddddddddddddddddddddd",
                status.HTTP_400_BAD_REQUEST,
            ),
            # test valid phone number and password
            (pytest.lazy_fixture("random_email"), pytest.lazy_fixture("random_password"), status.HTTP_201_CREATED),
        ],
    )
    def test_email_and_password_validation(
        self, api_client: APIClient, data_for_user: dict, email: str, password: str, http_status: status
    ):
        data_for_user["email"] = email
        data_for_user["password"] = data_for_user["password2"] = password
        response = api_client.post(FINAL_REGISTRATION_URL, data_for_user)
        assert response.status_code == http_status

    def test_passwords_not_match(self, api_client: APIClient, data_for_user: dict, random_password: str):
        data_for_user["password"] = random_password
        data_for_user["password2"] = random_password + "1"
        response = api_client.post(REGISTRATION_URL, data_for_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_passwords_match(self, api_client: APIClient, data_for_user: dict, random_password: str):
        data_for_user["password"] = data_for_user["password2"] = random_password
        response = api_client.post(FINAL_REGISTRATION_URL, data_for_user)
        assert response.status_code == status.HTTP_201_CREATED


class TestStepsRegistration:
    def test_first_step_registration(self, api_client: APIClient, first_step_registration_data: dict):
        response = api_client.post(REGISTRATION_URL, data=first_step_registration_data)
        assert response.status_code == status.HTTP_200_OK

    def test_second_step_registration(self, api_client: APIClient, second_step_registration_data: dict):
        response = api_client.post(REGISTRATION_URL, data=second_step_registration_data)
        assert response.status_code == status.HTTP_200_OK

    def test_third_step_registration(
        self,
        api_client: APIClient,
        second_step_registration_data: dict,
        third_step_registration_data: dict,
        random_otp: str,
        redis_cleaner: None,
    ):
        response = api_client.post(REGISTRATION_URL, data=second_step_registration_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Otp send, check your email"
        response1 = api_client.post(REGISTRATION_URL, data=second_step_registration_data | {"otp_code": random_otp})
        assert response1.status_code == status.HTTP_400_BAD_REQUEST
        response2 = api_client.post(REGISTRATION_URL, data=second_step_registration_data | {"otp_code": random_otp})
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        response3 = api_client.post(REGISTRATION_URL, data=second_step_registration_data | {"otp_code": random_otp})
        assert response3.status_code == status.HTTP_400_BAD_REQUEST
        response4 = api_client.post(REGISTRATION_URL, data=second_step_registration_data | {"otp_code": random_otp})
        assert response4.status_code == status.HTTP_400_BAD_REQUEST
        assert response4.json()["otp_code"] == [
            "Please try again or request a new code. You have only 3 attempts to write correct OTP code"
        ]


def test_correct_otp_and_confirmation_email(
    api_client: APIClient, success_third_step_registration: dict, random_otp: str, redis_cleaner: None
):
    response = api_client.post(REGISTRATION_URL, data=success_third_step_registration | {"otp_code": "111111"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User activated successfully."


def test_send_confirm_to_email(random_email: str, mailoutbox: list):
    email_subject = "Confirm your email"
    email_message = "Please click the link to confirm your email"
    user_email = random_email

    send_confirm_to_email(email_subject, email_message, user_email)

    assert len(mailoutbox) == 1
    email = mailoutbox[0]
    assert email.subject == email_subject
    assert email.body == email_message
    assert email.from_email == os.environ.get("HOST_USER")
    assert email.to == [user_email]
