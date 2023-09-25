import pytest
from django.contrib.auth.hashers import make_password

from app.settings import redis_client_confirm_otp
from user.models import User


@pytest.fixture(name="user_data")
def add_user_data(
    random_password: str,
    random_passport_id: str,
    random_birth_date: str,
    random_first_name: str,
    random_last_name: str,
    random_phone_number: str,
    random_email: str,
) -> User:
    hashed_password = make_password(random_password)
    user_data = User.objects.create(
        first_name=random_first_name,
        last_name=random_last_name,
        passport_id=random_passport_id,
        birth_date=random_birth_date,
        email=random_email,
        phone_number=random_phone_number,
        password=hashed_password,
    )
    user_data.save()
    return user_data


@pytest.fixture(name="data_for_user")
def data_for_user(
    random_password: str,
    random_passport_id: str,
    random_birth_date: str,
    random_first_name: str,
    random_last_name: str,
    random_phone_number: str,
    random_email: str,
) -> dict:
    redis_client_confirm_otp.set(random_email, random_email)
    data = {
        "first_name": random_first_name,
        "last_name": random_last_name,
        "passport_id": random_passport_id,
        "birth_date": random_birth_date,
        "email": random_email,
        "phone_number": random_phone_number,
        "password": random_password,
        "password2": random_password,
    }
    return data
