import json
import logging
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Set up logging
logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = 'WebSocketIds'

def lambda_handler(event, context):
    logger.info('$connect event: ' + json.dumps(event, indent=2))
    logger.info(f'$connect event["requestContext"]["connectionId"]: {event["requestContext"]["connectionId"]}')

    id = event['requestContext']['connectionId']
    item = {'id': id,
            'timestamp': int(datetime.now().strftime("%s"))}
            
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        logger.info(f'store id to dynamodb: {id}')
        table.put_item(Item=item)
    except ClientError as e:
        logger.error(e)
        raise ConnectionAbortedError(e)

    response = {'statusCode': 200}
    return response
