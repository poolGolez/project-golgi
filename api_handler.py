import boto3
import json
import os

dynamodb = boto3.client("dynamodb")
metadata_table = os.environ["METADATA_TABLE"]


def list(event, context):
    response = dynamodb.scan(
        TableName=metadata_table,
        Limit=50
    )
    body = parse_items(response["Items"])

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }


def get(event, context):
    id = event["pathParameters"]["id"]
    response = dynamodb.get_item(
        TableName=metadata_table,
        Key={
            "id": {"S": id}
        }
    )

    if not "Item" in response:
        return {"statusCode": 404}

    item = parse_record(response["Item"])
    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }


def parse_items(items):
    return [parse_record(item) for item in items]


def parse_record(item):
    return {
        "id": item["id"]["S"],
        "file_location": item["file_location"]["S"],
        "thumbnail_location": item["thumbnail_location"]["S"],
        "file_size": int(item["file_size"]["N"]),
        "_self": f"/api/files/{ item['id']['S'] }"
    }
