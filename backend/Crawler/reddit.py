import praw
import boto3

r = praw.Reddit(client_id = client, client_secret = secret, user_agent="pinkyshellha")
page = r.subreddit('nba')
top_posts = page.hot(limit=None)

table_name = "NBAReddit"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

for post in top_posts:
    item = { "id": post.id, 
             "title": post.title, 
             "url": post.url,
             "ups": post.ups,
             "downs": post.downs,
             "createdAt": int(post.created),
            }
    table.put_item(Item=item)
