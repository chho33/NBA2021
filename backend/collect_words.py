import boto3

table_name = "NBAReddit"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

data = [d["title"].strip() for d in table.scan()["Items"]]
data = " ".join(data)
with open("NBAWordCount.txt", "w") as f:
    f.write(data)

print(data)
