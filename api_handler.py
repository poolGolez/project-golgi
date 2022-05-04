import json

def list(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(event)
    }