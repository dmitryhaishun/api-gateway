import datetime
from decimal import Decimal

import pytest

from loan.helpers.enums import LoanCurrency, LoanProductType, LoanStage, LoanStatus


@pytest.fixture(name="mock_loans_data")
def loan_fixture() -> list:
    data = [
        {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "fk_loans_loan_products": 1,
            "loan_contract_number": "2222222222222222",
            "amount": 100,
            "currency": LoanCurrency.USD,
            "stage": LoanStage.NONE,
            "loan_term": datetime.timedelta(weeks=52),
            "loan_status": LoanStatus.DEBT,
            "loan_guarantors": "John Doe",
            "application_date": datetime.date.today(),
            "updated_at": datetime.date.today(),
            "apr": Decimal("5.1"),
            "paid_amount": 0,
        },
        {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "fk_loans_loan_products": 3,
            "loan_contract_number": "3333333333333333",
            "amount": 100,
            "currency": LoanCurrency.USD,
            "stage": LoanStage.NONE,
            "loan_term": datetime.timedelta(weeks=52),
            "loan_status": LoanStatus.PAID_OFF,
            "loan_guarantors": "John Doe",
            "application_date": datetime.date.today(),
            "updated_at": datetime.date.today(),
            "apr": Decimal("5.1"),
            "paid_amount": 0,
        },
    ]

    return data


@pytest.fixture(name="mock_loan_products")
def loan_products_fixture() -> list:
    data = [
        {
            "id": 1,
            "type": LoanProductType.STUDENT_LOAN,
            "description": "A loan for students",
            "loan_amount": [5000, 300000, 525000, 750000],
            "loan_term": ["1 year", "5 years", "15 years"],
            "apr": Decimal("7.1"),
        },
        {
            "id": 2,
            "type": LoanProductType.AUTO_LOAN,
            "description": "A loan for buying cars",
            "loan_amount": [5000, 300000, 525000, 750000],
            "loan_term": ["1 year", "5 years", "15 years"],
            "apr": Decimal("2"),
        },
        {
            "id": 3,
            "type": LoanProductType.MORTGAGE_LOAN,
            "description": "A loan for buying a house",
            "loan_amount": [5000, 300000, 525000, 750000],
            "loan_term": ["1 year", "5 years", "15 years"],
            "apr": Decimal("3.9"),
        },
    ]
    return data
