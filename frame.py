import os
import face_recognition
import pickle
import boto3
video_location ="D:\\Cloud_Computing\\cse546-project-lambda\\test_cases\\test_case_1\\test_7.mp4"
path = "D:\\Cloud_Computing\\CSE546_Project2\\"
image_path="D:\\Cloud_Computing\\CSE546_Project2\\test_7.jpg"

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    downloads3(bucket,key)
    video_location = "/tmp/" + key
    image_path = extract_frame(video_location)
    recognition(image_path)
    # uploads3("testfacerecogoutput",key)

def downloads3(s3_bucket_name, video_name):
    session = boto3.session.Session()
    s3_resource = session.resource("s3")
    file_name = "/tmp/" + video_name
    s3_resource.meta.client.download_file(s3_bucket_name,video_name,file_name)

def extract_frame(video_location):
    ##video_location is directory where videos are stored
    ##path is place where image will be downloaded
    video_name = video_location.rsplit(".",1)[0]
    file_name = video_name.rsplit("/")[2]
    file_name = file_name + ".jpg"
    os.system("ffmpeg -i " + str(video_location) + " -update 1 " + str(path) + file_name)
    image_path = os.path.abspath(file_name)
    return image_path


def recognition(image_path):
    image=face_recognition.load_image_file(image_path)
    image_encoding=face_recognition.face_encodings(image)[0]
    with open('D:\\Cloud_Computing\\cse546-project-lambda\\encoding.dat','rb') as f: ##figure out where .dat file will be in docker image
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
            print(face_names[idx])




# extract_frame(video_location,path)
# recognition(image_path)
