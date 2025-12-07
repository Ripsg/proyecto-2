import json
import os
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # API Gateway HTTP API envía el body como string JSON
    body_str = event.get("body", "{}")
    try:
        body = json.loads(body_str)
    except json.JSONDecodeError:
        body = {}

    name = body.get("name")
    drink = body.get("drink")
    size = body.get("size")

    if not name or not drink:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Faltan campos obligatorios (name, drink)"})
        }

    order_id = str(uuid4())
    item = {
        "orderId": order_id,
        "name": name,
        "drink": drink,
        "size": size or "medium",
        "createdAt": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Pedido registrado correctamente",
            "order": item
        })
    }
