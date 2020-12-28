import json
import boto3


def lambda_handler(event, context):
    bucket = event['Records'][0]["s3"]["bucket"]["name"]
    key = event['Records'][0]["s3"]["object"]["key"]
    client = boto3.client('rekognition')
    
    response=client.search_faces_by_image(
        CollectionId='faceCollection',
        Image={
            'S3Object':{
                'Bucket':bucket,
                'Name':key
            }
        },
        FaceMatchThreshold=80,
        MaxFaces=4
    )
    print(response)
    faceMatches=response['FaceMatches']
    if faceMatches is not None:
        for match in faceMatches:
            name = match['Face']['ExternalImageId']
            name = name.replace("_", " ")
            print(name)
            return {
                'statusCode': 200,
                'body': json.dumps(name)
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Unknown face! Please try again!')
        }
        
