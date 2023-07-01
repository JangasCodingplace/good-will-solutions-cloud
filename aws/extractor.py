import boto3
from configs import S3
from gwsf.exceptions import RawInfoException
from gwsf.functions import get_raw_data


def get_raw_info(storage_path: str) -> dict:
    client = boto3.client(service_name="textract")

    response = client.analyze_document(
        Document={
            "S3Object": {
                "Bucket": S3["bucket_name"],
                "Name": storage_path,
            },
        },
        FeatureTypes=["FORMS"],
    )

    return response


def send_data(raw_data: dict) -> dict:
    return raw_data


def get_exception(storage_path: str, exc: Exception):
    return RawInfoException(exc=exc, storage_path=storage_path)


def lambda_handler(event, contect):
    storage_path = event["Records"][0]["s3"]["object"]["key"]
    raw_data = get_raw_data(
        storage_path=storage_path,
        get=get_raw_info,
        send_data=send_data,
        get_exception=get_exception,
    )

    return {"statusCode": 200, "body": raw_data}
