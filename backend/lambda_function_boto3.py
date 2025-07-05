import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    
    elif http_method == 'POST':
        body = json.loads(event['body'])
        task = body['task']
        table.put_item(Item={
            'id': str(datetime.now().timestamp()),
            'task': task
        })
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Task added'})
        }
    
    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Invalid request'})
    }