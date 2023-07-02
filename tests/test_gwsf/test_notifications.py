from gwsf.functions import CreditApplication
from gwsf.notifications import get_service_message, get_supervisor_message


def test_get_service_message():
    application = CreditApplication(
        first_name="John",
        last_name="Smith",
        street="Samplestr. 42",
        city="London",
        zip_code="EC1A 1AA",
        country="England",
        application_date="01.01.2023",
        amount="42000",
        reason="Just for test purpose!",
        phone="1234578",
        email="test@jangascodingplace.com",
        timestamp=1672574400,
    )
    message = get_service_message(application=application)
    expected_message = "New Application received from Smith, John \namount: 42000"
    assert message == expected_message


def test_get_supervisor_message():
    application_1 = CreditApplication(
        first_name="John",
        last_name="Smith",
        street="Samplestr. 42",
        city="London",
        zip_code="EC1A 1AA",
        country="England",
        application_date="01.01.2023",
        amount="42000",
        reason="Just for test purpose!",
        phone="1234578",
        email="test@jangascodingplace.com",
        timestamp=1672574400,
    )
    application_2 = CreditApplication(
        first_name="John",
        last_name="Smith",
        street="Samplestr. 42",
        city="London",
        zip_code="EC1A 1AA",
        country="England",
        application_date="03.02.2023",
        amount="7000",
        reason="Just for test purpose!",
        phone="1234578",
        email="test@jangascodingplace.com",
        timestamp=1675425600,
    )
    supervisor_message = get_supervisor_message([application_1, application_2])
    expected_message = (
        "New Application received from Smith, John \n"
        "2023-01-01 - amount: 42000\n"
        "2023-02-03 - amount: 7000"
    )
    assert supervisor_message == expected_message
