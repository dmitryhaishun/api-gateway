import pytest
from faker import Faker

from account.models import ATM


@pytest.fixture(name="atm_data")
def all_atms_data(faker: Faker) -> dict:
    for _ in range(3):
        atm = ATM(
            country=faker.country(),
            city=faker.city(),
            address=faker.address(),
            atm_name=faker.street_name(),
            atm_number=faker.building_number(),
        )

        atm.save()
