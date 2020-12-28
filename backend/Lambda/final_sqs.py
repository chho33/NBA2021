import json
import boto3
import os
import time
from time import strptime
from datetime import datetime
import requests

def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    sqs = boto3.client('sqs', region_name= 'us-west-2')
    sns = boto3.client('sns')
    sqs2 = boto3.resource('sqs')
    queue = sqs2.get_queue_by_name(QueueName='Q1')
    queue_url = 'https://sqs.us-west-2.amazonaws.com/082676057290/Q1'
    
    new = []
    while True:
        response =  sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=30,
            WaitTimeSeconds=1
        )
        if 'Messages' in response: 
            for message in response['Messages']:
                receipt_handle = message['ReceiptHandle']
                js = json.loads(message['Body'])

                if('time' in js):
                    t = js['time']
                    phone = js['phone']
                    if(t < datetime.now().timestamp()):
                        m = "Hello, here is a reminder of your NBA game. The game will start in 5 minutes!"
                        sns.publish(PhoneNumber=str(phone), Message=m)
                    elif js not in new:
                        new.append(js)
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )
                else:
                    home = js['home']
                    visitor = js['visitor']
                    date = js['date']
                    phone = js['phone']
                    res = requests.get('http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard').json()
                    res_date = res['day']['date']
                    flag = True
                    if(res_date == date):
                      for e in res['events']:
                          if home == e['competitions'][0]['competitors'][0]['team']['displayName'] and visitor == e['competitions'][0]['competitors'][1]['team']['displayName']:
                              print(e['competitions'][0]['status']['type']['shortDetail'][-3:])
                              print(e['competitions'][0]['status']['clock'])
                              if e['competitions'][0]['status']['type']['shortDetail'][-3:] == "4th" and e['competitions'][0]['status']['clock']<300:
                                  m = "Hello, here is a reminder of your NBA game. The game between "+home+" and "+visitor+" is in last 5 minutes!"
                                  sns.publish(PhoneNumber=str(phone), Message=m)
                                  flag = False
                    if js not in new and flag == True:
                        new.append(js)
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )
        else:
            break
    print(new)
    for n in new:
        queue.send_message(MessageBody=json.dumps(n))