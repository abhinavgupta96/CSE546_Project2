import os

video_location ="/Users/abhinavgupta/Desktop/Code/Cloud\ Computing/cse546-project-lambda/test_cases/test_case_1/test_0.mp4"
path = "/Users/abhinavgupta/Desktop/Code/Cloud\ Computing/Project2/"

def extract_frame(video_location,path):
    ##video_location is directory where videos are stored
    ##path is place where image will be downloaded
    image_name = video_location.rsplit(".",1)[0]
    file_name = image_name.rsplit("/")[9] ## value - 9 is dependant on how many '/' are there in video_location 
    file_name = file_name + ".jpeg"
    os.system("ffmpeg -i " + str(video_location) + " -r 1 " + str(path) + file_name)
extract_frame(video_location,path)
