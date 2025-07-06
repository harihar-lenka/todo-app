import json
import boto3
import os
from uuid import uuid4

dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
table = dynamodb.Table(os.environ['TABLE_NAME'])


def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']

    if path == '/todos' and http_method == 'GET':
        try:
            response = table.scan()
            items = response['Items']
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps([{'id': item['id'], 'task': item['task'], 'completed': item['completed']} for item in items])
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': str(e)})
            }

    elif path == '/todos' and http_method == 'POST':
        try:
            body = json.loads(event['body'])
            task = body['task']
            item = {
                'id': str(uuid4()),
                'task': task,
                'completed': False
            }
            table.put_item(Item=item)
            return {
                'statusCode': 201,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(item)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': str(e)})
            }

    return {
        'statusCode': 400,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'error': 'Invalid request'})
    }
