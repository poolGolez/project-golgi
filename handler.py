import json
from re import S
import boto3
import uuid
import urllib.parse
import os
from PIL import Image

thumbnail_bucket = os.environ["THUMBNAIL_S3_BUCKET"]
thumbnail_size = int(os.environ["THUMBNAIL_SIZE"])
metadata_table = os.environ["METADATA_TABLE"]

s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")

def generate_thumbnail(event, context):
    print("Event", event)
    first_record = event["Records"][0]

    bucket_name = first_record["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(first_record["s3"]["object"]["key"], encoding='utf-8')
    s3_file_location = f"s3://{bucket_name}/{object_key}"
    object_size = first_record["s3"]["object"]["size"]

    resize_image(bucket_name, object_key)
    s3_thumbnail_location = f"s3://{thumbnail_bucket}/{object_key}"

    dynamodb.put_item(
        TableName=metadata_table,
        Item={
            "file_location": {"S": s3_file_location},
            "file_size": {"N": f"{object_size}"},
            "thumbnail_location": {"S": s3_thumbnail_location}
        }
    )

    body = {
        "message": "Success, buddy! You've got the S3 location",
        "s3": "{bucket_name}/{object_key}",
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def resize_image(bucket_name, object_key):
    filename = "/tmp/{}".format(uuid.uuid4())
    s3.download_file(bucket_name, object_key, filename)
    with Image.open(filename) as image:
        image.thumbnail((thumbnail_size, thumbnail_size))
        image.save(filename, "png")

    s3.upload_file(filename, thumbnail_bucket, object_key)
