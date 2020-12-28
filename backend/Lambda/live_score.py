import json
import logging
import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import base64
import hashlib

logging.basicConfig(format="%(levelname)s: %(asctime)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table_name = "WebSocketIds"
    record = event["records"]["live_score-0"][0]
    data = base64.b64decode(record["value"])
    logger.info(f"data: {data}")
    last_5_minute(data)

    api_client = boto3.client("apigatewaymanagementapi",
                               endpoint_url="https://k3pz0uagub.execute-api.us-west-2.amazonaws.com/dev/")
    #dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    items = table.scan()["Items"]
    for item in items:
        try:
            api_client.post_to_connection(Data=data,
                                          ConnectionId=item["id"])
        except ClientError as e:
            logger.error(e)

    response = {"statusCode": 200}
    return response


def last_5_minute(data):
    data = json.loads(data)
    start_time = str(data["start_time"])
    clock = int(data["clock"])
    logger.info(f"start_time: {start_time}" )
    logger.info(f"clock: {clock}")
    if start_time[-3:] == "4th" and clock < 300:
        logger.info("ready to send mail")
        send_mail(data)


def send_mail(data):
    hash_key = get_hash(data)
    logger.info(f"hash_key: {hash_key}")
    subscribers = [sub["sns"] for sub in get_subscribers(hash_key)]
    logger.info(f"subscribers: {subscribers}")
    if len(subscribers) > 0:
        for sub in get_send_list(hash_key, subscribers):
                send_sns(data, sub)


def get_hash(data):
    home = data["home"]
    visitor = data["visitor"]
    date = str(data["date"])
    text = f"{home}{visitor}{date}"
    hash_key = hashlib.md5(text.encode("utf-8")).hexdigest()
    return hash_key


def get_subscribers(hash_key):
    logger.info(f"get_subscribers")
    table_name = "NBANotify"
    #dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    res = table.query(KeyConditionExpression=Key("id").eq(hash_key))
    logger.info(f"get_subscribers res: {res}")
    return res["Items"]


def get_send_list(hash_key, subscribers):
    table_name = "NBANotified"
    #dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    res = table.query(KeyConditionExpression=Key("id").eq(hash_key))
    logger.info(f"get_send_list res: {res}")
    has_sent = [d["sns"] for d in res["Items"]]
    
    send_list = []
    for sub in subscribers:
        if sub not in has_sent:
            send_list.append(sub)

    logger.info(f"send_list: {send_list}")
    return send_list
        

def send_sns(data, phone):
    home = data["home"]
    visitor = data["visitor"]
    home_score = data["home_score"]
    visitor_score = data["visitor_score"]
    msg = f"{home} score: {home_score}; {visitor} score: {visitor_score}"
    sub = f"Notify: {home} v.s. {visitor}"
    
    sns = boto3.client("sns")
    response = sns.publish(
        PhoneNumber= phone,
        Message=msg
    )
    
    #topic_arn="arn:aws:sns:us-west-2:082676057290:NBA"
    #response = sns.publish (
    #    TopicArn=topic_arn,
    #    Message=msg,
    #    Subject=sub
    #)
    logger.info(f"response: {response}")
    
    table_name = "NBANotified"
    #dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    hash_key = get_hash(data)
    table.put_item(Item={"id": hash_key, "sns": phone})
