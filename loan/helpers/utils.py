from loan.helpers.enums import LoanType, LoanCurrency


def choose_loan_type() -> list:
    return [status.value for status in LoanType]


def choose_currency() -> list:
    return [currency.value for currency in LoanCurrency]
