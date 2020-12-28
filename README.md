# NBA 2021

## Table of Content
- [Overview](#Overview)
- [Features](#Features)
    - [Live Score](#Live-Score)
    - [Odds](#Odds)
    - [Chatbot](#Chatbot)
    - [Game Notify](#Game-Notify)
    - [Photo Recognition](#Photo-Recognition)
    - [Word Cloud](#Word-Cloud)
- [Architecture](#Architecture)
    - [Overall](#Overall)
    - [Kafka+EMR](#Kafka+EMR)
    - [WebSocket Live Score](#WebSocket-Live-Score)
- [Tools We Use](#Core-Features-and-Tools)
    - [CICD](#CICD)
    - [Events / Images Recognition](#Events-/-Images-Recognition)
    - [Live score / Game Notify](#Live-score-/-Game-Notify)
    - [Word Cloud](#Word-Cloud)
    - [Hybrid Cloud](#Hybrid-Cloud)
    - [Web Crawler](#Web-Crawler)
    - [Chatbot](#Chatbot)
    - [Other AWS Services](#Other-AWS-Services)
- [Demo Video](#Demo-Video)


## Overview
This is the website for NBA enthusiasts to keep track of up-to-date game information. We also provide notification service that helps you not missing any important event and game prograss.


## Features

### Live Score
<img src="https://i.imgur.com/KIoTyAj.gif" width="550">

- Our website provide the up-to-date live score for each game.

### Odds
<img src="https://i.imgur.com/5uVsEbC.png" width="550">

- Users who interest in sport lottery can use our service to monitor the odds for in-coming games.

### Chatbot
- Users can search for a player's statistics
- Or search the schedule of games.

### Game Notify
<img src="https://i.imgur.com/aDuhQU3.png" width="120">

- Users can get SNS message 5 minutes before a game starts.
- Or when a game in last 5 minutes.

### Photos Rekognition
<img src="https://i.imgur.com/Xy0Gbgf.png" width="550">

- Users can upload a player's (unknown) image and get his statistics.
- Users can upload a screenshot of a game (from Youtube) and get the detailed result of the game.

### Word Cloud
<img src="https://i.imgur.com/BdwBJpd.png" width="550">

- Show some popular keywords from Reddit.


## Architechture 
### Overall
![](https://i.imgur.com/vfFs25x.png)

### Kafka+EMR
![](https://i.imgur.com/FZevM8f.png)


### WebSocket Live Score
![](https://i.imgur.com/himaHBf.png)


## Tools We Use

### CICD

- CloudFormation: Defining the architectures by the cloudformation template.
    - `main.yaml`
    - `Lambda.yaml`
    - `lex.yaml`
    - `msk.yaml`
- CodePipeline: Using Seperate codepipelin binding different github branch to isolate front-end and back-end development.
    - `main.yaml` - WebPipeline binds frontend branch.
    - `main.yaml` - LambdaPipeline binds backend branch.
- Openapi: Defining apis by the openapi template.
    - `openapi.yaml`
    - `upload_player_photo.yaml`

### Events / Images Recognition
- Amazon Rekognition
    - Support searching player by their photo
    - Support searching games by Youtube snapshot
    - `backend/Lambda/final_rekognition.py`, `backend/Lambda/final_rekognition_text.py`

### Live score / Game Notify
- Amazon Managed Streaming for Kafka (MSK): In this project, we allocate two nodes in private subnet for Kafka broker. Besides, there is an extra node in public subnet as a rest-api server. The live_score topic on the broker keeps receiving message from a web crawler, and trigger a corresponding Lambda function to update the score on a webpage.
    - `msk.yaml`
- API Gateway (proxy): As a proxy for the client to send message to the kafka.
- API Gateway (web socket): To send the live score to the client immediately, this API Gateway manage the web socket resources. Once a client link to a web socket hosted by it, it builds an alive connection between the client and the server.
    - `backend/Lambda/websocket_connect.py`
    - `backend/Lambda/websocket_disconnect.py`
    - `backend/Lambda/live_score.py`
- Lambda Functions: Once the Kafka broker receives a message of a topic, Its corresponding Lambda functions will be triggered to execute some commands.
    - `backend/Lambda/live_score.py`
- SQS: Monitoring the time schedule of a game and trigger the Lambda to notify the subscribers for some events.
    - `backend/Lambda/final_sqs.py`
- SNS: For sending message to subscribers.
    - `backen/Lambda/live_score.py`

### Word Cloud
- Spark on EMR: Assuming a huge amount of text data need to be handle in the future, we adopt Apache Spark on the EMR clustr platform. To generate word counts for the word cloud, first, we scratch the text data from reddit to the word_count topic on the Kafka broker. A Lambda function then be triggered to execute one time EMR service to calculate the word counts by the Spark.
    - Trigger: `backend/Lambda/send_wordcount.py`, `backend/Lambda/update_wordcount.py`
    - Spark Function: `backend/NBAWordCount.py`
    - Output: `backend/NBAWordCount.txt`

### Hybrid Cloud
- VPC
    - Private Subnet
    - Public Subnet
- Route Table and Route
- NAT
- Internet Gateway

All set in `msk.yaml`.

### Web Crawler
- CloudWatch Event: To set the web crawler schedule.
- Lambda
    - `backend/Lambda/live_score_crawler.py`
    - `backend/Crawler/reddit.py`

### Chatbot
- Lex
    - Build: `backend/lexutils.py`, `backend/lex-manager.py`, `backend/bot-definition.json`
    - Functions: `backend/Lambda/final_lex.py`
    - Intents: Greeting Intent, Booking Intent, Search Game Intent, Search Player Intent

### DataBase
We use DynamoDB to host different types of data. The following are tables we use.
- Season: Basic game statistics.
- NBANotify: Recording different services subsbribed by different users.
- NBANotified: Recording some events already notified to avoid notifying repeatedly.
- NBAReddit: Text data crawled from reddit.
- NBAWordCloud: Storing the newest calculated word counts by Spark.
- player: NBA player information.
- WebSocketIds: Once a client connect to our live score page, a new web socket id is created. We record it for later live score pushing. Whenever the connection is closed, the id will be deleted.

### Other AWS Services
- S3 for hosting the website and store some assets and data.
- Cognito for uploading images to S3 bucket.
- IAM for unauthenticated roles under Amazon Cognito Identity pool.

### Demo Video
[Click Me](https://www.youtube.com/embed/JEi1qssEkVg)
