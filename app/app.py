import boto3
import json


def update_event_rule(message_body):
    """ Updates the event rule using a cron expression. """

    year = message_body['schedule']['year']
    month = message_body['schedule']['month']
    day = message_body['schedule']['day']
    hour = message_body['schedule']['hour']
    minute = message_body['schedule']['minute']

    cron_expression = f'cron({minute} {hour} {day} {month} ? {year})'

    # Update the rule
    client = boto3.client('events')

    client.put_rule(
    Name = "rule-test-lambda-every-minute",
    ScheduleExpression = cron_expression,
    State = "ENABLED"
)

def lambda_handler(event,context):
    """ Handles the initial request. """

    for record in event['Records']:
        message_body = record['body']

        # Replace the single backslashes with double
        message_body = message_body.replace("\'", "\"")

        # Convert the string response to JSON object
        message_body = json.loads(message_body)

        # Update the event rule
        update_event_rule(message_body)



if __name__ == '__main__':

    # Create the events payload
    event_change_rule = {
        "Records": [
            {
                "body": "{'schedule':{'year': '2022','month': '2','day': '28','hour': '22','minute': '21'}}"
            }
        ]
    }

    # Trigger the lambda handler
    lambda_handler(event_change_rule, '')