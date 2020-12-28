import requests
from datetime import datetime

res = requests.get('http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard').json()
"""
odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': '8699dfb86a358ebfc4983fa7e23661ef',
        'sport': 'basketball_nba',
        'region': 'us'
    })
odd_res = odds_response.json()
"""
#print(res)
date = res['day']['date']
event = []
for i, e in enumerate(res['events']):
    data = {}
    data['venue'] = e['competitions'][0]['venue']['fullName']
    data['city'] = e['competitions'][0]['venue']['address']['city']
    data['state'] = e['competitions'][0]['venue']['address']['state']
    
    data['home'] = e['competitions'][0]['competitors'][0]['team']['displayName']
    data['visitor'] = e['competitions'][0]['competitors'][1]['team']['displayName']
    
    data['home_link'] = e['competitions'][0]['competitors'][0]['team']['links'][2]['href']
    data['visitor_link'] = e['competitions'][0]['competitors'][1]['team']['links'][2]['href']
    
    data['home_logo'] = e['competitions'][0]['competitors'][0]['team']['logo']
    data['visitpr_logo'] = e['competitions'][0]['competitors'][1]['team']['logo']
    
    data['home_score'] = e['competitions'][0]['competitors'][0]['score']
    data['visitor_score'] = e['competitions'][0]['competitors'][1]['score']
    
    data['start_time'] = e['competitions'][0]['status']['type']['shortDetail']
    data['clock'] = e['competitions'][0]['status']['clock']
    data['displayClock'] = e['competitions'][0]['status']['displayClock']
    #print(data)
    for d in data:
        print(d+" : "+str(data[d]))
        
        
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('2019-20season')
    response = table.query(
            IndexName='home-index',
            KeyConditionExpression=Key('home').eq(data['home'].lower())
        )
    history = []
    for r in response['Items']:
        if(r['visitor'] == data['visitor'].lower()):
            history.append(r)
    response = table.query(
            IndexName='home-index',
            KeyConditionExpression=Key('home').eq(data['visitor'].lower())
        )
    for r in response['Items']:
        if(r['visitor'] == data['home'].lower()):
            history.append(r)
            
            
    table = dynamodb.Table('2017-19season')
    response = table.query(
            IndexName='home-index',
            KeyConditionExpression=Key('home').eq(data['home'].lower())
        )
    for r in response['Items']:
        if(r['visitor'] == data['visitor'].lower()):
            history.append(r)
    response = table.query(
            IndexName='home-index',
            KeyConditionExpression=Key('home').eq(data['visitor'].lower())
        )
    for r in response['Items']:
        if(r['visitor'] == data['home'].lower()):
            history.append(r)
    
    history.sort(key=lambda x:(x['date'][-4:], datetime.strptime(x['date'][4:-5], "%b %d")), reverse = True)

    print(history)
    
    
    #print("\n\n\n")
    """
    bet = []
    r = odd_res['data'][i]
    if(data['home'] == r['teams'][0]):
        for site in r['sites']:
            b = {}
            b['website'] = site['site_nice']
            b['odds'] = site['odds']['h2h']
            bet.append(b)
    else:
        for site in r['sites']:
            b = {}
            b['website'] = site['site_nice']
            b['odds'] = site['odds']['h2h']
            b['odds'][0], b['odds'][1] = b['odds'][1], b['odds'][0]
            bet.append(b)
    print(bet)
    """