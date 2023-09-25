import pytest


@pytest.fixture(name="mock_data_cards")
def cards_fixture() -> list:
    data = [
        {
            "id": 1,
            "user_uuid": "ebb106b5-8605-4985-b29c-75f15efb0c36",
            "card_product_id": 1,
            "number": "4560574142720341",
            "cardholder_name": "Anastasia Bialystockaya",
            "status": "ISSUANCE",
            "expiration_date": "2025-01-01",
            "payment_system": "MASTERCARD",
            "account_number": "05 2191 3601 1111 1112 5868 2762",
            "cvv": "026",
            "cash_withdraw_limit": None,
            "card_to_card_limit": None,
            "expenses_limit": None,
            "block_reason": None,
            "created_at": "2023-07-11",
            "issue_term": "2023-07-13",
            "pin": "2779",
        },
        {
            "id": 1,
            "user_uuid": "ebb106b5-8605-4985-b29c-75f15efb0c36",
            "card_product_id": 1,
            "number": "8077846835337169",
            "cardholder_name": "Phillip Minskiy",
            "status": "ISSUANCE",
            "expiration_date": "2026-02-02",
            "payment_system": "MASTERCARD",
            "account_number": "16 3202 4712 2222 2223 6979 3873",
            "cvv": "723",
            "cash_withdraw_limit": None,
            "card_to_card_limit": None,
            "expenses_limit": None,
            "block_reason": None,
            "created_at": "2023-07-11",
            "issue_term": "2023-01-03",
            "pin": "6422",
        },
    ]
    return data


@pytest.fixture(name="mock_data_for_card")
def card_fixture(mock_data_cards) -> dict:
    return mock_data_cards[0]


@pytest.fixture(name="mock_data_card_products")
def card_products_fixture() -> list:
    data = [
        {
            "name": "card product 1",
            "available_currencies": None,
            "free_card_servicing": None,
            "issue_time": None,
            "additional_information": None,
            "active": True,
        },
        {
            "name": "card product 2",
            "available_currencies": None,
            "free_card_servicing": None,
            "issue_time": None,
            "additional_information": None,
            "active": True,
        },
    ]
    return data
