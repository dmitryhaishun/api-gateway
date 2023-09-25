from enum import StrEnum


class AccountType(StrEnum):
    CREDIT = "CREDIT"
    CURRENT = "CURRENT"
    DEPOSIT = "DEPOSIT"
    INTEREST = "INTEREST"


class Currency(StrEnum):
    EUR = "EUR"
    USD = "USD"
    # CHF = "CHF"
    # PLN = "PLN"
    # CZK = "CZK"
    # GBP = "GBP"
