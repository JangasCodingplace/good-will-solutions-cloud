from datetime import datetime

from gwsf.functions import CreditApplication
from gwsf.utils import parse_form_to_credit_application


def test_parse_form_to_credit_application():
    raw_form_data = {
        "family name": "Smith",
        "first name": "John",
        "street and street number": "123 Main St",
        "city": "New York",
        "postcode": "10001",
        "country": "USA",
        "date": "2023-07-01",
        "credit amount": 10000,
        "explain where you need the money for": "Home renovation",
        "phone": "555-1234",
        "email": "john@example.com",
    }

    expected_result = CreditApplication(
        timestamp=int(datetime.now().timestamp()),
        last_name="Smith",
        first_name="John",
        street="123 Main St",
        city="New York",
        zip_code="10001",
        country="USA",
        application_date="2023-07-01",
        amount=10000,
        reason="Home renovation",
        phone="555-1234",
        email="john@example.com",
    )

    result = parse_form_to_credit_application(raw_form_data)
    assert result.timestamp == expected_result.timestamp
    assert result.last_name == expected_result.last_name
    assert result.first_name == expected_result.first_name
    assert result.street == expected_result.street
    assert result.city == expected_result.city
    assert result.zip_code == expected_result.zip_code
    assert result.country == expected_result.country
    assert result.application_date == expected_result.application_date
    assert result.amount == expected_result.amount
    assert result.reason == expected_result.reason
    assert result.phone == expected_result.phone
    assert result.email == expected_result.email
