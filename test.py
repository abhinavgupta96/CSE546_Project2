import json
import boto3
import csv
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    downloads3(bucket,key)
    uploads3("testfacerecogoutput",key)

    # result = s3_resource.get_bucket_notification_configuration(Bucket=bucket_name)
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    # key = event['Records'][0]['s3']['object']['name']
    # file_name = "/tmp/" + key
    # s3_resource.meta.client.download_file(bucket_name,key,file_name)
    # s3_bucket_name = "testfacerecogoutput"
    # s3_resource.put_object(Bucket = s3_bucket_name, key=key, body = key)
    
    # TODO implement

def downloads3(s3_bucket_name, image_name):
    session = boto3.session.Session()
    s3_resource = session.resource("s3")
    file_name = "/tmp/" + image_name
    s3_resource.meta.client.download_file(s3_bucket_name,image_name,file_name)
    
def uploads3(s3_bucket_name,image_name):
    file_name = "/tmp/" + image_name
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3_bucket_name)
    response = bucket.upload_file(file_name, image_name)
    print(response)

def query_db(name):
    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.get_item(
    TableName="Project2",
    Key={
        'name': {'S': name}
    }
)
    print(response['Item'])
    return (response['Item'])

# def createoutput():
#     db_result = 
query_db("president_biden")