import json
import logging
import os
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = 'WebSocketIds'
def lambda_handler(event, context):
    logger.info('$disconnect event: ' + json.dumps(event, indent=2))
    logger.info(f'$disconnect event["requestContext"]["connectionId"]: {event["requestContext"]["connectionId"]}')

    id = event['requestContext']['connectionId']
    item = {'id': id}
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        table.delete_item(Key=item)
    except ClientError as e:
        logger.error(e)
        raise ValueError(e)

    response = {'statusCode': 200}
    return response
