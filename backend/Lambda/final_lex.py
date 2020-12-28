import json
import boto3
import os
import time
from time import strptime
from datetime import datetime
from boto3.dynamodb.conditions import Key


def modify(s):
    temp = s.split(" ")
    s = ""
    for t in temp:
        t = t[0].upper() + t[1:]+" "
        s+=t
    s = s[:-1]
    return s


def greet(intent_request):
    return {
        'dialogAction': {
            "type": "Close",
            "fulfillmentState": "Fulfilled", 
            'message': {
                'contentType': 'PlainText',
                'content': 'Hi there, how can I help you?\nYou can search player\'s statistics by entering his name.\nOr, you can search for a game.'
            }
        }
    }
    
def player(intent_request):
    slots = intent_request['currentIntent']['slots']
    first = slots['first_name']
    last = slots['last_name']
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('player')

    name = first.lower()+" "+last.lower()
    
    res = table.query(
        IndexName='name-index',
        KeyConditionExpression=Key('name').eq(name.lower())
    )
    if res['Items']:
        m = [None]*15
        m[0] = "Hi, here is the player's information"
        m[1] = f"Player name: {name}"
        m[2] = f"Player age: {res['Items'][0]['age']}"
        m[3] = "Team: "
        m[4] = "Position: "
        m[5] = "Game play: "
        m[6] = "Points per game: "
        m[7] = "Field goal percentage: "
        m[8] = "Free throw percentage: "
        m[9] = "3-point percentage: "
        m[10] = "Steals: "
        m[11] = "Rebounds: "
        m[12] = "Blocks: "
        m[13] = "Turnovers: "
        m[14] = "Assists: "
        for r in res['Items']:
            m[3]+=f" {r['team']}"
            m[4]+=f" {r['pos']}"
            m[5]+=f" {r['game']}"
            m[6]+=f" {str(r['points']/r['game'])[:5]}"
            m[7]+=f" {str(r['fg'])[:5]}"
            m[8]+=f" {str(r['ft'])[:5]}"
            m[9]+=f" {str(r['3p'])[:5]}"
            m[10]+=f" {r['steal']}"
            m[11]+=f" {r['rb']}"
            m[12]+=f" {r['block']}"
            m[13]+=f" {r['turnover']}"
            m[14]+=f" {r['assist']}"
        message = ""
        for mm in m:
            message+=mm
            message+="\n"
        #print(message)
        
        return {
            'sessionAttributes': intent_request['sessionAttributes'],
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',
                    'content': message
                }
            }
        }
    else:
        return {
            'sessionAttributes': intent_request['sessionAttributes'],
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Sorry, we can\'t find the player. Please try again'
                }
            }
        }

def game(intent_request):
    slots = intent_request['currentIntent']['slots']
    date = str(slots['date'])
    team = slots['team']
    season = slots['season']
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    time = ""
    now = datetime.now()
    year = 2020
    if(season == '2019-20'):
        table = dynamodb.Table('2019-20season')
        if(int(date[5:7]) > 10) or (int(date[5:7]) == 10 and int(date[8:])>20):
            time = datetime(2019, int(date[5:7]), int(date[8:]))
            year = 2019
        else:
            time = datetime(2020, int(date[5:7]), int(date[8:]))
    else:
        table = dynamodb.Table('2020-21season')
        if(int(date[5:7]) == 12):
            time = datetime(2020, int(date[5:7]), int(date[8:]))
        else:
            time = datetime(2021, int(date[5:7]), int(date[8:]))
            year = 2021
    if(team is None):
        q = time.strftime("%c")[0:10]+" "+time.strftime("%c")[-4:]
        if(int(date[8:])<10):
            q = q[:7]+q[8:]
        res = table.query(
            IndexName='date-index',
            KeyConditionExpression=Key('date').eq(q)
        )
        if res['Items'] and time < now:
            message = "Here are results on "+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)+":\n"
            for r in res['Items']:
                m = modify(r['home'])+"\t"+str(r['h_points'])+"\t"+modify(r['visitor'])+"\t"+str(r['v_points'])+"\n"
                message+=m
            print(message)
            return {
                'sessionAttributes': intent_request['sessionAttributes'],
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',                        
                        'content': message
                    }
                }
            }
        elif res['Items']:
            message = "Here are upcoming games on "+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)+":\n"
            for r in res['Items']:
                m = modify(r['home'])+"\t"+modify(r['visitor'])+"\t"+r['time']+"\n"
                message+=m
            print(message)
            return {
                'sessionAttributes': intent_request['sessionAttributes'],
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',                        
                        'content': message
                    }
                }
            }
        else:
            return {
                'sessionAttributes': intent_request['sessionAttributes'],
                'dialogAction': {
                    'type': 'Close', 
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',                        
                        'content': 'Sorry, we can\'t find any games on '+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)
                    }
                }
            }
    
    else:
        q = time.strftime("%c")[0:10]+" "+time.strftime("%c")[-4:]
        if(int(date[8:])<10):
            q = q[:7]+q[8:]
        res = table.query(
            IndexName='date-index',
            KeyConditionExpression=Key('date').eq(q)
        )
        if res['Items'] and time < now:
            message = "Here is game of "+modify(team)+" on "+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)+":\n"
            flag = False
            for r in res['Items']:
                if r['home']!= team and r['visitor']!= team:
                    continue
                flag = True
                m = modify(r['home'])+"\t"+str(r['h_points'])+"\t"+modify(r['visitor'])+"\t"+str(r['v_points'])+"\n"
                message+=m
            print(message)
            if(flag):
                return {
                    'sessionAttributes': intent_request['sessionAttributes'],
                    'dialogAction': {
                        'type': 'Close',
                        'fulfillmentState': 'Fulfilled',
                        'message': {
                            'contentType': 'PlainText',                        
                            'content': message
                        }
                    }
                }
            else:
                return {
                    'sessionAttributes': intent_request['sessionAttributes'],
                    'dialogAction': {
                        'type': 'Close', 
                        'fulfillmentState': 'Fulfilled',
                        'message': {
                            'contentType': 'PlainText',                        
                            'content': 'Sorry, we can\'t find a '+modify(team)+ ' game on '+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)
                        }
                    }
                }
        elif res['Items']:
            message = "Here is upcoming game of "+modify(team)+" on "+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)+":\n"
            flag = False
            for r in res['Items']:
                if r['home']!= team and r['visitor']!= team:
                    continue
                flag = True
                m = modify(r['home'])+"\t"+modify(r['visitor'])+"\t"+r['time']+"\n"
                message+=m
            print(message)
            if(flag):
                return {
                    'sessionAttributes': intent_request['sessionAttributes'],
                    'dialogAction': {
                        'type': 'Close',
                        'fulfillmentState': 'Fulfilled',
                        'message': {
                            'contentType': 'PlainText',                        
                            'content': message
                        }
                    }
                }
            else:
                return {
                    'sessionAttributes': intent_request['sessionAttributes'],
                    'dialogAction': {
                        'type': 'Close', 
                        'fulfillmentState': 'Fulfilled',
                        'message': {
                            'contentType': 'PlainText',                        
                            'content': 'Sorry, we can\'t find a '+modify(team)+ ' game on '+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)
                        }
                    }
                }
        else:
            return {
                'sessionAttributes': intent_request['sessionAttributes'],
                'dialogAction': {
                    'type': 'Close', 
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',                        
                        'content': 'Sorry, we can\'t find a '+modify(team)+ ' game on '+time.strftime("%B")+" "+time.strftime("%d")+" "+str(year)
                    }
                }
            }

def book(intent_request):
    slots = intent_request['currentIntent']['slots']
    date = slots['date']
    team = slots['team']
    decision = slots['decision']
    phone = slots['phone']
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('2020-21season')
    sqs = boto3.resource('sqs')
    sns = boto3.client('sns')
    queue = sqs.get_queue_by_name(QueueName='Q1')
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    temp = datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
    q = temp.strftime("%c")[0:10]+" "+temp.strftime("%c")[-4:]
    if(int(date[8:])<10):
        q = q[:7]+q[8:]
    res = table.query(
        IndexName='date-index',
        KeyConditionExpression=Key('date').eq(q)
    )
    ans = {}
    for r in res['Items']:
        if r['home']!= team and r['visitor']!= team:
            continue
        else:
            ans = r
    if ans:
        if decision == "(1)":
            date = ans['date']
            d = date.split(" ")
            t = ans['time']
            t= t[:-1].split(":")
            if(t[0] == "12"):
                t[0] = "0"
            sec = datetime(int(d[3]), int(strptime(d[1],'%b').tm_mon), int(d[2]), int(t[0])+12, int(t[1]))
            queue.send_message(
                MessageBody=json.dumps({
                    'time': sec.timestamp()-300,
                    'phone': phone
                })
            )
            return {
                'sessionAttributes': intent_request['sessionAttributes'],
                'dialogAction': {
                    'type': 'Close', 
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',                        
                        'content': "You\'re all set!"
                    }
                }
            }
        elif decision == "(2)":
            queue.send_message(
                MessageBody=json.dumps({
                    'date': slots['date'],
                    'home': modify(ans['home']),
                    'visitor': modify(ans['visitor']),
                    'phone': phone
                })
            )
            return {
                'sessionAttributes': intent_request['sessionAttributes'],
                'dialogAction': {
                    'type': 'Close', 
                    'fulfillmentState': 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',                        
                        'content': 'We have received your last 5 minutes alarm request! Enjoy your game!'
                    }
                }
            }
    else:
        return {
            'sessionAttributes': intent_request['sessionAttributes'],
            'dialogAction': {
                'type': 'Close', 
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',                        
                    'content': 'Sorry, we can\'t find a '+modify(team)+ ' game on '+time.strftime("%B")+" "+time.strftime("%d")+" "+time.strftime("%Y")
                }
            }
        }
    
def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'greeting':
        return greet(intent_request)
    elif intent_name == 'search_game':
        return game(intent_request)
    elif intent_name == 'search_player':
        return player(intent_request)
    elif intent_name == 'book':
        return book(intent_request)

def lambda_handler(event, context):
    return dispatch(event)
