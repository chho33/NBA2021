instanceType=m1.small
instanceType=m4.large

aws emr create-cluster \
     --name NBAWordCount \
     --release-label emr-5.31.0 \
     --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=$instanceType InstanceGroupType=CORE,InstanceCount=1,InstanceType=$instanceType\
     --service-role EMR_DefaultRole \
     --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole,SubnetId=subnet-0a9ea60c98b4ac104,KeyName=coms6998\
     --log-uri s3://nba.assets \
     --enable-debugging \
     --no-auto--terminate \
     --visible-to-all-users \
     --applications Name=Hadoop Name=Spark \
     --region us-west-2 
