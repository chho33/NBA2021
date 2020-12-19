aws s3 rm s3://nba.assets --recursive
aws s3 rm s3://nba.website --recursive
aws cloudformation delete-stack --stack-name NBALambda 
aws cloudformation delete-stack --stack-name NBA 
