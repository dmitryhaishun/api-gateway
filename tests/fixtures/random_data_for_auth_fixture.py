import random
import re
import string

import pytest
from faker import Faker


@pytest.fixture(name="random_first_name")
def random_first_name_fixture(faker: Faker) -> str:
    return faker.first_name()


@pytest.fixture(name="random_last_name")
def random_last_name_fixture(faker: Faker) -> str:
    return faker.last_name()


@pytest.fixture(name="random_email")
def random_email_fixture(faker: Faker) -> str:
    return faker.email()


@pytest.fixture(name="random_birth_date")
def random_birth_date_fixture(faker: Faker) -> str:
    return faker.date_of_birth(minimum_age=18, maximum_age=65)


@pytest.fixture(name="random_phone_number")
def random_phone_number_fixture(faker: Faker) -> str:
    def generate_phone_number() -> str:
        phone_number = faker.phone_number()
        clean_phone_number = "+" + "".join(filter(str.isdigit, phone_number))
        if 12 <= len(clean_phone_number) <= 13:
            return clean_phone_number
        return generate_phone_number()

    return generate_phone_number()


@pytest.fixture(name="random_password")
def random_password_fixture(faker: Faker) -> str:
    def generate_password() -> str:
        password = faker.password(special_chars=True, digits=True, upper_case=True, lower_case=True)
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&+])[A-Za-z\d@$!%*?&+]{6,20}$", password):
            return password
        return generate_password()

    return generate_password()


@pytest.fixture(name="random_passport_id")
def random_passport_number_fixture() -> str:
    def generate_passport_number() -> str:
        passport_length = random.randint(6, 20)
        passport_characters = string.ascii_uppercase + string.digits
        passport = "".join(random.choice(passport_characters) for _ in range(passport_length))
        if 5 < len(passport) < 20:
            return passport
        return generate_passport_number()

    return generate_passport_number()


@pytest.fixture(name="random_otp")
def generate_random_otp() -> int:
    return random.randint(100000, 999999)
