import json
import urllib.request
import urllib.parse
import hashlib
import hmac
import base64
from datetime import datetime
import time

# AWS DynamoDB configuration
REGION = 'us-east-1'
SERVICE = 'dynamodb'
HOST = f'dynamodb.{REGION}.amazonaws.com'
ENDEVENT = f'https://{HOST}/'
TABLE_NAME = 'Tasks'


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region, service):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region)
    k_service = sign(k_region, service)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


def lambda_handler(event, context):
    # AWS credentials from Lambda environment (set by IAM role)
    access_key = context.identity.access_key
    secret_key = context.identity.secret_key

    # Prepare request signing
    method = event['httpMethod']
    amz_date = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    date_stamp = amz_date[:8]

    # Canonical request components
    canonical_uri = '/'
    canonical_querystring = ''
    canonical_headers = f'host:{HOST}\nx-amz-date:{amz_date}\n'
    signed_headers = 'host;x-amz-date'

    if method == 'GET':
        # DynamoDB Scan operation
        payload = json.dumps({
            'TableName': TABLE_NAME
        })
        headers = {
            'Content-Type': 'application/x-amz-json-1.0',
            'X-Amz-Target': 'DynamoDB_20120810.Scan',
            'Host': HOST,
            'X-Amz-Date': amz_date
        }
    elif method == 'POST':
        # DynamoDB PutItem operation
        body = json.loads(event['body'])
        task = body['task']
        item_id = str(time.time())
        payload = json.dumps({
            'TableName': TABLE_NAME,
            'Item': {
                'id': {'S': item_id},
                'task': {'S': task}
            }
        })
        headers = {
            'Content-Type': 'application/x-amz-json-1.0',
            'X-Amz-Target': 'DynamoDB_20120810.PutItem',
            'Host': HOST,
            'X-Amz-Date': amz_date
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid request'})
        }

    # Create canonical request
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    canonical_request = f'{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

    # Create string to sign
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = f'{date_stamp}/{REGION}/{SERVICE}/aws4_request'
    string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}'

    # Sign the request
    signing_key = get_signature_key(secret_key, date_stamp, REGION, SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode(
        'utf-8'), hashlib.sha256).hexdigest()

    # Add authorization header
    headers['Authorization'] = f'{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'

    # Make HTTP request
    req = urllib.request.Request(ENDPOINT, data=payload.encode(
        'utf-8'), headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            if method == 'GET':
                items = json.loads(response_body).get('Items', [])
                return {
                    'statusCode': 200,
                    'body': json.dumps(items)
                }
            elif method == 'POST':
                return {
                    'statusCode': 201,
                    'body': json.dumps({'message': 'Task added'})
                }
    except urllib.error.HTTPError as e:
        return {
            'statusCode': e.code,
            'body': json.dumps({'message': str(e)})
        }
