import json

import pytest
from aws.send_application_to_service_department import (
    parse_dynamodb_event_to_application,
    parse_dynamodb_event_to_dict,
)

from . import FIXTURE_DIR


@pytest.fixture
def dynamo_db_event():
    with open(FIXTURE_DIR / "dynamodb_create_applicant_event.json", "r") as f:
        data = json.load(f)
    return data


def test_parse_dynamodb_event_to_dict(dynamo_db_event):
    d = parse_dynamodb_event_to_dict(event=dynamo_db_event["Records"][0]["dynamodb"])
    assert d.get("country") == "GERMANY "
    assert d.get("reason") == "1 am at a strange place and try to come back home. "
    assert d.get("amount") == "12000 "
    assert d.get("city") == "MUNCHEN "
    assert d.get("phone") == "+4917612342421 "
    assert d.get("street") == "Am HARRAS 12 "
    assert d.get("application_date") == "01.07.2023 "
    assert d.get("last_name") == "SPARROW "
    assert d.get("first_name") == "JACK "
    assert d.get("email") == "sparrow63@gmail.com "
    assert d.get("zip_code") == "81373 "
    assert d.get("timestamp") == 1688325652


def test_parse_dynamodb_event_to_application(dynamo_db_event):
    # TODO - use mock for having a real unittest
    credit_application = parse_dynamodb_event_to_application(
        event=dynamo_db_event["Records"][0]["dynamodb"]
    )
    assert credit_application.country == "GERMANY "
    assert credit_application.reason == "1 am at a strange place and try to come back home. "
    assert credit_application.amount == "12000 "
    assert credit_application.city == "MUNCHEN "
    assert credit_application.phone == "+4917612342421 "
    assert credit_application.street == "Am HARRAS 12 "
    assert credit_application.application_date == "01.07.2023 "
    assert credit_application.last_name == "SPARROW "
    assert credit_application.first_name == "JACK "
    assert credit_application.email == "sparrow63@gmail.com "
    assert credit_application.zip_code == "81373 "
    assert credit_application.timestamp == 1688325652
