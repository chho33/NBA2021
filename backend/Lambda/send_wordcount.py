import json
import boto3
import requests

def lambda_handler(event, context):
    topic = "word_count"
    kafka_api = f"https://onfw57cah0.execute-api.us-west-2.amazonaws.com/dev/topics/{topic}"
    
    table_name = "NBAReddit"
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)    
    data = [d["title"].strip() for d in table.scan()["Items"]]
    data = " ".join(data)

    res = requests.post(
        url = kafka_api,
        headers = {"Content-Type": "application/vnd.kafka.json.v2+json"},
        json = {"records": [{"value": data}]}
    )
    
    response = {"statusCode": 200, "data": data, "res": res.text}
    return response
