import json

import pytest
from aws.store_raw_data import parse_raw_data

from . import FIXTURE_DIR


@pytest.fixture
def message():
    with open(FIXTURE_DIR / "msg_broker_raw_data.json", "r") as f:
        data = json.load(f)
    return data


def test_parser(message):
    credit_application = parse_raw_data(message)
    assert credit_application.first_name == "JACK "
    assert credit_application.last_name == "SPARROW "
    assert credit_application.street == "Am HARRAS 12 "
    assert credit_application.city == "MUNCHEN "
    assert credit_application.zip_code == "81373 "
    assert credit_application.country == "GERMANY "
    assert credit_application.application_date == "01.07.2023 "
    assert credit_application.amount == "12000 "
    assert credit_application.reason == "1 am at a strange place and try to come back home. "
    assert credit_application.phone == "+4917612342421 "
    assert credit_application.email == "sparrow63@gmail.com "
