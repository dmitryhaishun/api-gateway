import pytest

from app.settings import redis_client_check_otp as redis_client


@pytest.fixture(name="first_step_registration_data")
def first_step_data(
    random_first_name: str,
    random_last_name: str,
    random_birth_date: str,
    random_passport_id: str,
) -> dict:
    data = {
        "first_name": random_first_name,
        "last_name": random_last_name,
        "passport_id": random_passport_id,
        "birth_date": random_birth_date,
    }
    return data


@pytest.fixture(name="second_step_registration_data")
def second_step_data(
    first_step_registration_data: dict,
    random_phone_number: str,
    random_email: str,
) -> dict:
    data = first_step_registration_data | {
        "phone_number": random_phone_number,
        "email": random_email,
    }
    return data


@pytest.fixture(name="third_step_registration_data")
def third_step_data(second_step_registration_data: dict, random_otp: str) -> dict:
    data = second_step_registration_data | {
        "otp_code": random_otp,
    }
    return data


@pytest.fixture(name="fourth_step_registration")
def fourth_step_data(third_step_registration_data: dict, random_password: str) -> dict:
    data = third_step_registration_data | {"password": random_password, "password2": random_password}
    return data


@pytest.fixture(name="success_third_step_registration")
def success_third_step(second_step_registration_data: dict, random_password: str, random_email: str) -> dict:
    second_step_registration_data["email"] = random_email
    redis_client.set(random_email, "111111")
    data = second_step_registration_data | {"password": random_password, "password2": random_password}
    return data
