import json
from re import S
import boto3
import urllib.parse

s3 = boto3.client("s3")

def generate_thumbnail(event, context):
    first_record = event["Records"][0]

    bucket_name = first_record["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(first_record["s3"]["object"]["key"], encoding='utf-8')

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    s3_object = response["Body"].read()

    body = {
        "message": "Success, buddy! You've got the S3 location",
        "s3": "{bucket_name}/{object_key}",
    }

    return {"statusCode": 200, "body": json.dumps(body)}
