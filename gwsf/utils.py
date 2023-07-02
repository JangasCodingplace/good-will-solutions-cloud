from datetime import datetime

from .functions import CreditApplication


def parse_form_to_credit_application(raw_form_data: dict) -> CreditApplication:
    """Parse raw form data into a CreditApplication object.

    This function takes a dictionary of raw form data and maps the
    keys to their corresponding values in the desired format for a
    CreditApplication. The mapping is defined by the `mapper`
    dictionary, which associates the keys in the raw form data with
    the corresponding keys in the CreditApplication object.

    TODO: add levenshtein distance if a key is missing

    Parameters:
    -----------
        raw_form_data (dict): A dictionary containing raw form data.

    Returns:
    --------
        CreditApplication: An instance of the CreditApplication class
        populated with the parsed data.
    """
    mapper = {
        "last_name": "family name",
        "first_name": "first name",
        "street": "street and street number",
        "city": "city",
        "zip_code": "postcode",
        "country": "country",
        "application_date": "date",
        "amount": "credit amount",
        "reason": "explain where you need the money for",
        "phone": "phone",
        "email": "email",
    }
    d = {}
    for key, value in raw_form_data.items():
        for k, v in mapper.items():
            if v in key.lower():
                d[k] = value
                break

    credit_application = CreditApplication(timestamp=int(datetime.now().timestamp()), **d)
    return credit_application
