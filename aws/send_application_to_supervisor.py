import boto3
from configs import DYNAMO_DB, SENDER_MAIL, SUPERVISOR_MAIL
from boto3.dynamodb.conditions import Key
from gwsf.exceptions import SupervisorMessageException
from gwsf.functions import CreditApplication, send_application_to_supervisor_if_required
from gwsf.notifications import get_supervisor_message, send_sendgrid_notifications


def parse_dynamodb_event_to_dict(event: dict):
    d = {}
    for key, value in event["NewImage"].items():
        d[key] = value.get("S") or int(value.get("N", 0))
    return d


def parse_dynamodb_event_to_application(event: dict):
    return CreditApplication(**parse_dynamodb_event_to_dict(event))


def query_applicants(credit_application: CreditApplication) -> list[CreditApplication]:
    dynamo_db_client = boto3.resource(
        service_name="dynamodb",
    )
    table_name = DYNAMO_DB["applicant_table_name"]
    table = dynamo_db_client.Table(table_name)
    response = table.query(KeyConditionExpression=Key("email").eq(credit_application.email))
    all_applications = [
        CreditApplication(timestamp=int(row.pop("timestamp")), **row) for row in response["Items"]
    ]
    return all_applications


def send_message(message: str):
    return send_sendgrid_notifications(
        content=message,
        subject="Recurring Credit Application Detected",
        sender=SENDER_MAIL,
        receiver=SUPERVISOR_MAIL,
    )


def get_exception(entity: dict, exc: Exception):
    return SupervisorMessageException(exc=exc, entity=entity)


def lambda_handler(event, contect):
    status, text = send_application_to_supervisor_if_required(
        message=event["Records"][0]["dynamodb"],
        parse_db_entity=parse_dynamodb_event_to_application,
        fetch_from_db=query_applicants,
        get_message=get_supervisor_message,
        send_message=send_message,
        get_exception=get_exception,
    )
    if status >= 400:
        raise ValueError(text)
    return {"statusCode": 200}
