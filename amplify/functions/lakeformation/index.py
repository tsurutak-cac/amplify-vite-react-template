import json


def handler(event, context):
    return {
        "statusCode": 200,
        # Modify the CORS settings below to match your specific requirements
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Restrict this to domains you trust
            "Access-Control-Allow-Headers": "*",  # Specify only the headers you need to allow
        },
        "body": json.dumps({
            "message": "Hello World",
        }),
    }
