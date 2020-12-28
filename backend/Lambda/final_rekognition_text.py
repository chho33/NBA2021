import json
import boto3
from boto3.dynamodb.conditions import Key

team = {
    'ATL': 'Atlanta Hawks',
    'HAWKS': 'Atlanta Hawks',
    'BKN': 'Brooklyn Nets',
    'NETS': 'Brooklyn Nets',
    'BOS': 'Boston Celtics',
    'CELTICS': 'Boston Celtics',
    'CHA': 'Charlotte Hornets',
    'HORNETS': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'BULLS': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'CAVALIERS': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'MAVERICKS': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'NUGGETS': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'PISTONS': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'WARRIORS': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'ROCKETS': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'PACERS': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'CLIPPERS': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'LAKERS': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'GRIZZLIES': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'HEAT': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'BUCKS': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'TIMBERWOLVES': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NO': 'New Orleans Pelicans',
    'PELICANS': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'KNICKS': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'THUNDERS': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'MAGIC': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    '76ERS': 'Philadelphia 76ers',
    '76ers': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'SUNS': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'BLAZERS': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'KINGS': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'SA': 'San Antonio Spurs',
    'SPURS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'RAPTORS': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'UTAH': 'Utah Jazz',
    'JAZZ': 'Utah Jazz',
    'WAS': 'Washington Wizards',
    'WSH': 'Washington Wizards',
    'WIZARDS': 'Washington Wizards'
}

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def lambda_handler(event, context):
    bucket = event['Records'][0]["s3"]["bucket"]["name"]
    key = event['Records'][0]["s3"]["object"]["key"]
    client=boto3.client('rekognition')

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':key}})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    res = []
    geo = []
    score = []
    flag = False
    str = ""
    dec = 0.000
    dec2 = 0.000
    for text in textDetections:
        if 'DetectedText' in text:
            #print('now:', text)
            if flag == True and RepresentsInt(text['DetectedText']):
                flag = False
                score.append(text['DetectedText'])
                res.append(str)
                geo.append(dec)
                geo.append(dec2)
            if text['DetectedText'] in team:
                if team[text['DetectedText']] not in res:
                    print('now:', text)
                    flag = True
                    #res.append(team[text['DetectedText']])
                    #geo.append(text['Geometry']['BoundingBox']['Left'])
                    str = team[text['DetectedText']]
                    dec = text['Geometry']['BoundingBox']['Left']
                    dec2 = text['Geometry']['BoundingBox']['Top']
                    #print(team[text['DetectedText']])
    if(geo[0] > geo[2] and geo[0]-geo[2] >0.03) or (geo[1] > geo[3] and geo[1]-geo[3] > 0.03):
        temp = res[0]
        res[0] = res[1]
        res[1] = temp
        temp = score[0]
        score[0] = score[1]
        score[1] = temp
    print(res)
    print(score)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('2019-20season')
    data = table.query(
        IndexName='visitor-index',
        KeyConditionExpression=Key('visitor').eq(res[0].lower())
    )
    ans = []
    for d in data['Items']:
        if(d['home'] == res[1].lower()):
            if(len(score) == 2):
                if(int(score[0]) <= int(d['v_points']) and int(score[1]) <= int(d['h_points'])):
                    a = {
                        'h_points': int(d['h_points']), 
                        'date': d['date'], 
                        'v_points': int(d['v_points']), 
                        'time': d['time'], 
                        'visitor': d['visitor'], 
                        'attend': int(d['attend']), 
                        'home': d['home']
                    }
                    ans.append(a)
            else:    
                a = {
                    'h_points': int(d['h_points']), 
                    'date': d['date'], 
                    'v_points': int(d['v_points']), 
                    'time': d['time'], 
                    'visitor': d['visitor'], 
                    'attend': d['attend'], 
                    'home': d['home']
                }
                ans.append(a)
    print(ans)
    return {
        'statusCode': 200,
        'body': json.dumps(ans)
    }
