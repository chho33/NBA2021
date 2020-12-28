import json
import logging
logging.basicConfig(format="%(levelname)s: %(asctime)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def emr_trigger():
    conn = boto3.client("emr")        
    cluster_id = conn.run_job_flow(
        Name='NBAWordCloud',
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        VisibleToAllUsers=True,
        LogUri='s3://nba.assets',
        ReleaseLabel='emr-5.32.0',
        Instances={
            'MasterInstanceType': 'm4.large',
            'SlaveInstanceType': 'm4.large',
            'InstanceCount': 1,
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False,
            'Ec2SubnetId': 'subnet-aabbd4cf',
            'Ec2KeyName': 'coms6998',
        },
        Applications=[{
            'Name': 'Spark'
        }],
        Configurations=[{
            "Classification":"spark-env",
            "Properties":{},
            "Configurations":[{
                "Classification":"export",
                "Properties":{
                    "PYSPARK_PYTHON":"/usr/bin/python3",
                }
            }]
        }],
        BootstrapActions=[{
            'Name': 'Install',
            'ScriptBootstrapAction': {
                'Path': 's3://nba.assets/python_packages.sh'
            }
        }],
        Steps=[{
            'Name': 'NBAWordCloud',
            'ActionOnFailure': 'TERMINATE_CLUSTER',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    "spark-submit",
                    "--driver-memory", "2g",
                    #"--deploy-mode", "cluster",
                    "--deploy-mode", "client",
                    "--num-executors", '1',
                    "--executor-cores", '1',
                    "--py-files", "s3://nba.assets/NBAWordCount.py",
                    's3://nba.assets/NBAWordCount.py', 's3://nba.assets/NBAWordCount.txt', 'stop_words.txt'
                ]
            }
        }],
    )


def lambda_handler(event, context):
    record = event["records"]["word_count-0"][0]
    data = base64.b64decode(record["value"])
    logger.info(f"data: {data}")
    
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=data.encode('utf-8'), Bucket='nba.assets', Key='NBAWordCount.txt')
    emr_trigger()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
