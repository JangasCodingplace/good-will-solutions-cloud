import os

S3 = {
    "bucket_name": os.getenv("S3_BUCKET_NAME"),
}


DYNAMO_DB = {
    "applicant_table_name": os.getenv("DYNAMO_DB_APPLICANT_TABLE_NAME"),
}


SUPERVISOR_MAIL = os.getenv("SUPERVISOR_MAIL", "contact@janisgoesser.com")
SENDER_MAIL = os.getenv("SENDER_MAIL", "info@jangascodingplace.com")
