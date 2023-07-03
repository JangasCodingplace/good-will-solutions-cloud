from gwsf.exceptions import ServiceMessageException
from gwsf.functions import CreditApplication, send_application_to_service_department
from gwsf.notifications import get_service_message, send_discord_notifications


def parse_dynamodb_event_to_dict(event: dict):
    d = {}
    for key, value in event["NewImage"].items():
        d[key] = value.get("S") or int(value.get("N", 0))
    return d


def parse_dynamodb_event_to_application(event: dict):
    return CreditApplication(**parse_dynamodb_event_to_dict(event))


def get_exception(entity: dict, exc: Exception):
    return ServiceMessageException(exc=exc, entity=entity)


def lambda_handler(event, contect):
    status, text = send_application_to_service_department(
        message=event["Records"][0]["dynamodb"],
        parse_db_entity=parse_dynamodb_event_to_application,
        get_message=get_service_message,
        send_message=send_discord_notifications,
        get_exception=get_exception,
    )
    if status >= 400:
        raise ValueError(text)
    return {"statusCode": 200}
