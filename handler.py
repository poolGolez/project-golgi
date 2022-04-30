import json
from re import S
import boto3
import uuid
import urllib.parse
import os
from PIL import Image

s3 = boto3.client("s3")
thumbnail_bucket = os.environ["THUMBNAIL_S3_BUCKET"]
thumbnail_size = int(os.environ["THUMBNAIL_SIZE"])

def generate_thumbnail(event, context):
    print("Event", event)
    first_record = event["Records"][0]

    bucket_name = first_record["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(first_record["s3"]["object"]["key"], encoding='utf-8')

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    s3_object = response["Body"].read()

    filename = "/tmp/{}".format(uuid.uuid4())
    s3.download_file(bucket_name, object_key, filename)
    resize_image(filename)
    s3.upload_file(filename, thumbnail_bucket, object_key)

    body = {
        "message": "Success, buddy! You've got the S3 location",
        "s3": "{bucket_name}/{object_key}",
    }

    return {"statusCode": 200, "body": json.dumps(body)}

def resize_image(image_path):
    with Image.open(image_path) as image:
        image.thumbnail((thumbnail_size, thumbnail_size))
        image.save(image_path, "png")
