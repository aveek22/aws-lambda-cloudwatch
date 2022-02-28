import boto3
import json
from datetime import datetime as dt
import pytz



def update_event_rule(message_body):
    """ Updates the event rule using a cron expression. """

    year = message_body['schedule']['year']
    month = message_body['schedule']['month']
    day = message_body['schedule']['day']
    hour = message_body['schedule']['hour']
    minute = message_body['schedule']['minute']
    tz_offset = message_body['tz_offset']

    # Datetime string and format
    dttm_str = f'{year}-{month}-{day} {hour}:{minute}:00 {tz_offset}'
    dttm_format = f'%Y-%m-%d %H:%M:%S %z'

    # Generate datetime from string
    event_dttm_local = dt.strptime(dttm_str, dttm_format)
    print(f'Local Time: {event_dttm_local}')
    # event_dttm_local = event_dttm_local.replace(tzinfo=pytz.timezone(local_tz))
    # print(f'Local Time with Timezone: {event_dttm_local}')

    # Convert local datetime to UTC
    event_dttm_utc = event_dttm_local.astimezone(pytz.UTC)
    print(f'UTC Time: {event_dttm_utc}')

    # Generate the cron expression for UTC event datetime
    cron_expression = f'cron({event_dttm_utc.minute} {event_dttm_utc.hour} {event_dttm_utc.day} {event_dttm_utc.month} ? {event_dttm_utc.year})'

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
                "body": "{'schedule':{'year': '2022','month': '3','day': '1','hour': '00','minute': '2'},'tz_offset':'+0100'}"
            }
        ]
    }

    # Trigger the lambda handler
    lambda_handler(event_change_rule, '')