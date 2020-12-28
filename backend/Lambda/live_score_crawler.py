import requests
from datetime import datetime
import logging

logging.basicConfig(format="%(levelname)s: %(asctime)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


kafka_api = "https://onfw57cah0.execute-api.us-west-2.amazonaws.com/dev/topics/live_score"

def lambda_handler(event, context):
    res = requests.get('http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard').json()
    logger.info(f"res: {res}")
    
    date = res['day']['date']
    event = []
    e = res['events'][0]
    data = {}
    data['venue'] = e['competitions'][0]['venue']['fullName']
    data['city'] = e['competitions'][0]['venue']['address']['city']
    data['state'] = e['competitions'][0]['venue']['address']['state']

    data['home'] = e['competitions'][0]['competitors'][0]['team']['displayName']
    data['visitor'] = e['competitions'][0]['competitors'][1]['team']['displayName']

    data['home_link'] = e['competitions'][0]['competitors'][0]['team']['links'][2]['href']
    data['visitor_link'] = e['competitions'][0]['competitors'][1]['team']['links'][2]['href']

    data['home_logo'] = e['competitions'][0]['competitors'][0]['team']['logo']
    data['visitor_logo'] = e['competitions'][0]['competitors'][1]['team']['logo']

    data['home_score'] = e['competitions'][0]['competitors'][0]['score']
    data['visitor_score'] = e['competitions'][0]['competitors'][1]['score']

    data['start_time'] = e['competitions'][0]['status']['type']['shortDetail']
    data['clock'] = e['competitions'][0]['status']['clock']
    data['displayClock'] = e['competitions'][0]['status']['displayClock']
    data['date'] = date

    logger.info(f"data: {data}")
    res = requests.post(
        url = kafka_api,
        headers = {"Content-Type": "application/vnd.kafka.json.v2+json"},
        json = {"records": [{"value": data}]}
    )
    
    
    response = {"statusCode": 200, "data": data, "res": res.text}
    return response
