import json
from collections import defaultdict
from dataclasses import asdict

import boto3
from configs import DYNAMO_DB
from gwsf import functions as f
from gwsf.exceptions import StoreDataException
from gwsf.functions import CreditApplication
from gwsf.utils import parse_form_to_credit_application


class AWSTextract:
    """Helper class for parsing AWS textracts form response to a
    key-value dictionary

    The code is more or less completely copied from an official
    example by AWS:
    https://docs.aws.amazon.com/textract/latest/dg/examples-extract-kvp.html
    """

    @staticmethod
    def get_kv_map(blocks: list[dict]) -> tuple[dict, dict, dict]:
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

    @staticmethod
    def find_value_block(key_block: dict, value_map: dict) -> dict:
        for relationship in key_block["Relationships"]:
            if relationship["Type"] == "VALUE":
                for value_id in relationship["Ids"]:
                    value_block = value_map[value_id]
        return value_block

    @staticmethod
    def get_text(result: dict, blocks_map: dict) -> str:
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

    @staticmethod
    def get_kv_relationship(key_map, value_map, block_map):
        kvs = defaultdict(list)
        for _, key_block in key_map.items():
            value_block = AWSTextract.find_value_block(key_block, value_map)
            key = AWSTextract.get_text(key_block, block_map)
            val = AWSTextract.get_text(value_block, block_map)
            kvs[key].append(val)
        return kvs

    @staticmethod
    def parse_blocks_to_dict(blocks: list[dict]) -> dict:
        key_map, value_map, block_map = AWSTextract.get_kv_map(blocks)
        key_values = AWSTextract.get_kv_relationship(key_map, value_map, block_map)
        parsed_data = {key: value[0] for key, value in key_values.items()}
        return parsed_data


def parse_raw_data(raw_data: dict) -> CreditApplication:
    textract_response_blocks = raw_data["responsePayload"]["body"]["Blocks"]
    raw_textract_dict = AWSTextract.parse_blocks_to_dict(textract_response_blocks)
    credit_application = parse_form_to_credit_application(raw_textract_dict)
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
