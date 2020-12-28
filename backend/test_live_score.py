import requests as req
import random
from time import sleep

kafka_api = "https://onfw57cah0.execute-api.us-west-2.amazonaws.com/dev/topics/live_score"

data = {"venue": "AmericanAirlines Arena",
        "city": "Miami",
        "state": "FL",
        "home": "Los Angeles Clippers",
        "visitor": "Dallas Mavericks",
        "home_link": "http://www.espn.com/nba/team/stats/_/name/mia/miami-heat",
        "visitor_link": "http://www.espn.com/nba/team/stats/_name/no/new-orleans-pelicans",
        "home_logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/mia.png",
        "visitor_logo": "https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/no.png",
        "home_score": 0,
        "visitor_score": 0,
        "start_time": "12/25 - 12:00 4th",
        "clock": 599,
        "displayClock": "4:46",
        "date": "2020-12-27"
}

for i in range(30):
    home_score = random.choice([0,2,3])
    visitor_score = random.choice([0,2,3])
    if i%2 == 0: 
        data["visitor_score"] += visitor_score
    else:
        data["home_score"] += home_score
    data["clock"] -= 10 
    print(data)
    res = req.post(
        url = kafka_api,
        headers = {"Content-Type": "application/vnd.kafka.json.v2+json"},
        json = {"records": [{"value": data}]}
    )
    sleep(0.5)
