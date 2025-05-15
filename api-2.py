import boto3
import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

schedules = {}
sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/276784368250/my-api-queue"

class Schedules(Resource):
    def get(self):
        return schedules

    def post(self):
        schedule = request.get_json()
        new_id = max(schedules.keys(), default=0) + 1
        schedule["id"] = new_id
        schedules[new_id] = schedule
        
        # Enviar mensaje a SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "action": "create_schedule",
                "payload": schedule
            })
        )
        return {new_id: schedule}, 201

api.add_resource(Schedules, '/schedules')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
