region=us-west-2
clusterArn=arn:aws:kafka:us-west-2:082676057290:cluster/MSKCluster/c4979ec5-758a-4531-88f9-54f3825225d5-8

aws kafka describe-cluster --region $region --cluster-arn $clusterArn > kafka.config

aws kafka get-bootstrap-brokers --region $region --cluster-arn $clusterArn > bootstrap-brokers.config
