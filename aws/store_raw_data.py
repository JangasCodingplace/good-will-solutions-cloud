import json
from collections import defaultdict
from dataclasses import asdict

import boto3
from configs import DYNAMO_DB
from gwsf import functions as f
from gwsf.exceptions import StoreDataException
from gwsf.functions import CreditApplication


def parse_raw_data(raw_data: dict) -> CreditApplication:
    # methods are copied from
    # https://docs.aws.amazon.com/textract/latest/dg/examples-extract-kvp.html

    def get_kv_map(blocks):
        # get key and value maps
        key_map = {}
        value_map = {}
        block_map = {}
        for block in blocks:
            block_id = block["Id"]
            block_map[block_id] = block
            if block["BlockType"] == "KEY_VALUE_SET":
                if "KEY" in block["EntityTypes"]:
                    key_map[block_id] = block
                else:
                    value_map[block_id] = block

        return key_map, value_map, block_map

    def find_value_block(key_block, value_map):
        for relationship in key_block["Relationships"]:
            if relationship["Type"] == "VALUE":
                for value_id in relationship["Ids"]:
                    value_block = value_map[value_id]
        return value_block

    def get_text(result, blocks_map):
        text = ""
        if "Relationships" in result:
            for relationship in result["Relationships"]:
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        word = blocks_map[child_id]
                        if word["BlockType"] == "WORD":
                            text += word["Text"] + " "
                        if word["BlockType"] == "SELECTION_ELEMENT":
                            if word["SelectionStatus"] == "SELECTED":
                                text += "X "

        return text

    def get_kv_relationship(key_map, value_map, block_map):
        kvs = defaultdict(list)
        for _, key_block in key_map.items():
            value_block = find_value_block(key_block, value_map)
            key = get_text(key_block, block_map)
            val = get_text(value_block, block_map)
            kvs[key].append(val)
        return kvs

    def parse_to_applicant_dict(raw_data: dict):
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
        }
        d = {}
        for key, value in raw_data.items():
            for k, v in mapper.items():
                if v in key.lower():
                    d[k] = value
                    break
        return d

    textract_response_blocks = raw_data["responsePayload"]["body"]["Blocks"]
    key_map, value_map, block_map = get_kv_map(textract_response_blocks)
    key_values = get_kv_relationship(key_map, value_map, block_map)
    parsed_data = {key: value[0] for key, value in key_values.items()}
    credit_application = CreditApplication(**parse_to_applicant_dict(parsed_data))
    return credit_application


def store_raw_data(credit_application: CreditApplication):
    dynamo_db_client = boto3.resource(service_name="dynamodb")
    table_name = DYNAMO_DB["applicant_table_name"]
    table = dynamo_db_client.Table(table_name)
    item = asdict(credit_application)
    return table.put_item(Item=item)


def get_exception(raw_data: dict, exc: Exception):
    return StoreDataException(raw_data=raw_data, exc=exc)


def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        f.store_raw_data(
            raw_data=message,
            parse=parse_raw_data,
            store=store_raw_data,
            get_exception=get_exception,
        )

    return {
        "statusCode": 200,
        "body": "",
    }
