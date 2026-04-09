import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    # Get current count
    response = table.get_item(Key={"id": "visitor_count"})

    # If item exists, increment. If not, start at 1
    if "Item" in response:
        count = int(response["Item"]["count"]) + 1
    else:
        count = 1

    # Update the count in DynamoDB
    table.update_item(
        Key={"id": "visitor_count"},
        UpdateExpression="SET #c = :val",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":val": count},
    )

    # Return count with CORS headers (so your website can call this API)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"visitor_count": count}),
    }