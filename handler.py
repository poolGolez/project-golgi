import json
import urllib.parse

def generate_thumbnail(event, context):

    first_record = event["Records"][0]

    bucket_name = first_record["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(first_record["s3"]["object"]["key"], encoding='utf-8')
    body = {
        "message": "Success, buddy! You've got the S3 location",
        "s3": "{bucket_name}/{object_key}",
    }

    return {"statusCode": 200, "body": json.dumps(body)}
