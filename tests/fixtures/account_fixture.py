from _pytest.fixtures import fixture

from account.helpers.enums import AccountType


@fixture(name="mock_accounts_data")
def accounts_fixture() -> list:
    data = [
        {
            "number": "1234567890123450",
            "user_uuid": "03275756-5b65-4930-9f9e-0898d713ca60",
            "currency": "usd",
            "amount": 100,
            "account_type": AccountType.CREDIT,
        },
        {
            "number": "1234567890123451",
            "user_uuid": "03275756-5b65-4930-9f9e-0898d713ca61",
            "currency": "eur",
            "amount": 10001,
            "account_type": AccountType.CURRENT,
        },
        {
            "number": "1234567890123452",
            "user_uuid": "03275756-5b65-4930-9f9e-0898d713ca62",
            "currency": "pln",
            "amount": 66666,
            "account_type": AccountType.DEPOSIT,
        },
        {
            "number": "1234567890123453",
            "user_uuid": "03275756-5b65-4930-9f9e-0898d713ca63",
            "currency": "byn",
            "amount": 770000,
            "account_type": AccountType.INTEREST,
        },
        {
            "number": "1234567890123454",
            "user_uuid": "03275756-5b65-4930-9f9e-0898d713ca60",
            "currency": "usd",
            "amount": 555555,
            "account_type": AccountType.CURRENT,
        },
    ]
    return data


@fixture(name="mock_account_data")
def account_fixture(mock_accounts_data) -> dict:
    return mock_accounts_data[0]
