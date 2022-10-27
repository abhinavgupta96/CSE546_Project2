import boto3
import csv

BUCKET_NAME = "studentdataoutput"


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


def createCSV(fileName, name):
    with open(fileName + ".csv", "a") as f:
        writer = csv.writer(f)
        student_data = query_db("mr_bean")
        name = student_data['name']['S']
        major = student_data['major']['S']
        year = student_data['year']['S']
        writer.writerow([name, major, year])


def uploads3(s3_bucket_name, file_name):
    file_name = file_name + ".csv"
    s3_client = boto3.client("s3")
    s3_client.upload_file(file_name, s3_bucket_name, file_name)


fileName = "test"
name = "mr_bean"

createCSV(fileName, name)
uploads3(BUCKET_NAME, fileName)
