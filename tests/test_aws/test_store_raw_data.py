import json

import pytest
from aws.store_raw_data import parse_raw_data
from gwsf.functions import CreditApplication

from . import FIXTURE_DIR


@pytest.fixture
def message():
    with open(FIXTURE_DIR / "msg_broker_raw_data.json", "r") as f:
        data = json.load(f)
    return data


def test_parser(message):
    credit_application = parse_raw_data(message)
    expected_credit_application = CreditApplication(
        first_name="BILL ",
        last_name="GATED ",
        street="1835 73rd Ave NE ",
        city="MEDINA ",
        zip_code="98111 ",
        country="United States ",
        application_date="28.06.2023 ",
        amount="10000 ",
        reason="A big investment in an Al company has put me in a financially difficult position ",
    )
    assert credit_application == expected_credit_application
