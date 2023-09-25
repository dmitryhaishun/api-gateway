from .fixtures.account_fixture import account_fixture, accounts_fixture
from .fixtures.atm_fixture import all_atms_data
from .fixtures.base_fixture import api_client, db_for_all_test, redis_cleaner
from .fixtures.card_fixture import card_fixture, card_products_fixture, cards_fixture
from .fixtures.data_for_adding_to_auth_database_fixture import add_user_data, data_for_user
from .fixtures.data_for_all_steps_auth_fixture import (
    first_step_data,
    fourth_step_data,
    second_step_data,
    success_third_step,
    third_step_data,
)
from .fixtures.loan_fixture import loan_fixture, loan_products_fixture
from .fixtures.random_data_for_auth_fixture import (
    generate_random_otp,
    random_birth_date_fixture,
    random_email_fixture,
    random_first_name_fixture,
    random_last_name_fixture,
    random_passport_number_fixture,
    random_password_fixture,
    random_phone_number_fixture,
)
