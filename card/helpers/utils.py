import random

from card.helpers.enums import Branch, CardProducts, Currency, PaymentSystem


def choose_currency() -> list:
    print("AAAAAAAA", [currency.value for currency in Currency])
    return [currency.value for currency in Currency]


def choose_branch() -> list:
    return [branch.value for branch in Branch]


def choose_product() -> list:
    return [product.value for product in CardProducts]


def choose_payment_system() -> list:
    return [system.value for system in PaymentSystem]


def get_account_number() -> str:
    return str(random.randint(0, 9999999999999999)).zfill(16)


# def choose_account_number() -> list:
#     return [system.value for system in PaymentSystem]
