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


def parse_items(items):
    return [{
        "id": item["id"]["S"],
        "file_location": item["file_location"]["S"],
        "thumbnail_location": item["thumbnail_location"]["S"],
        "file_size": int(item["file_size"]["N"]),
        "_self": f"/api/files/{ item['id']['S'] }"
    } for item in items]
