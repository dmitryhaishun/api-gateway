import pytest
from faker import Faker
from rest_framework.test import APIClient

from app.settings import redis_client_check_otp as redis_client


@pytest.fixture(name="faker")
def faker_fixture() -> Faker():  # type: ignore # [valid-type]
    fake = Faker()
    return fake


@pytest.fixture()
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(autouse=True, scope="function")
def db_for_all_test(db: None) -> None:
    pass


@pytest.fixture(scope="function", name="redis_cleaner")
def redis_cleaner():
    yield redis_client
    redis_client.select(1)
    redis_client.flushdb()
