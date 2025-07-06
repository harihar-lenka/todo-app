from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from prometheus_client import Counter, generate_latest
import os

app = Flask(__name__)
CORS(app)

# Prometheus metrics
requests_total = Counter('http_requests_total',
                         'Total HTTP Requests', ['endpoint'])

# DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
table = dynamodb.Table(os.environ['TABLE_NAME'])


@app.route('/metrics')
def metrics():
    requests_total.labels(endpoint='/metrics').inc()
    return generate_latest()


@app.route('/todos', methods=['GET'])
def get_todos():
    requests_total.labels(endpoint='/todos').inc()
    response = table.scan()
    items = response['Items']
    return jsonify([{'id': item['id'], 'task': item['task'], 'completed': item['completed']} for item in items])


@app.route('/todos', methods=['POST'])
def add_todo():
    requests_total.labels(endpoint='/todos').inc()
    data = request.get_json()
    task = data['task']
    item = {
        'id': str(hash(task + str(os.urandom(16)))),  # Simple unique ID
        'task': task,
        'completed': False
    }
    table.put_item(Item=item)
    return jsonify(item), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
