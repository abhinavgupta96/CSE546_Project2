import os
import face_recognition
import pickle
import boto3
import csv


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    downloads3(bucket,key)
    video_location = "/tmp/" + key
    image_path = extract_frame(video_location)
    face_name = recognition(image_path)
    csv_file_name = createCSV(key,face_name)
    uploads3("outputface",csv_file_name)

def downloads3(s3_bucket_name, video_name):
    session = boto3.session.Session()
    s3_resource = session.resource("s3")
    file_name = "/tmp/" + video_name #location inside docker container will be /home/app/
    s3_resource.meta.client.download_file(s3_bucket_name,video_name,file_name)

def extract_frame(video_location):
    ##video_location is directory where videos are stored
    ##path is place where image will be downloaded
    print(video_location)
    video_name = video_location.rsplit(".",1)[0]
    file_name = video_name.rsplit("/")[2]
    file_name = file_name + ".jpeg"
    print(file_name)
    path = "/tmp/"
    os.system("ffmpeg -i " + str(video_location) + " -update 1 " + str(path) + file_name)
    print(os.path.isfile("/tmp/"+ file_name))
    image_path = "/tmp/" + file_name
    print(image_path)
    return image_path



def recognition(image_path):
    image=face_recognition.load_image_file(image_path)
    image_encoding=face_recognition.face_encodings(image)[0]
    encoding_path = "/home/app/encoding.dat"
    with open(encoding_path,'rb') as f: ##figure out where .dat file will be in docker image
        all_face_encodings=pickle.load(f)
        face_names=list(all_face_encodings.keys())
        face_encodings=list(all_face_encodings.values())
        #print(face_encodings[0])
        face_names=face_encodings[0]
    #print(face_names)
    #print("-----------------------------------------------------------")
    #print((all_face_encodings)['encoding'])
    face_encodings=all_face_encodings['encoding']
    result=face_recognition.compare_faces(face_encodings,image_encoding)
    for res in result:
        if res:
            idx=result.index(res)
            return(face_names[idx]) ##add return statement

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


def createCSV(videoName, face_name):
    video_name = videoName.rsplit(".",1)[0]
    file_name = "/tmp/" + video_name + ".csv"
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        student_data = query_db(face_name)
        name = student_data['name']['S']
        major = student_data['major']['S']
        year = student_data['year']['S']
        writer.writerow([name, major, year])
    print(os.path.isfile(file_name))
    return file_name


def uploads3(s3_bucket_name,csv_name):
    file_name = csv_name
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3_bucket_name)
    response = bucket.upload_file(file_name, csv_name)
    print("File uploaded")