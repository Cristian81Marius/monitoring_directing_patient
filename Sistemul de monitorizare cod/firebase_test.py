from datetime import datetime
from picamera import PiCamera
from time import sleep
from subprocess import call
import os
import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyAyGwesvzexk9GkSziuUoUnm5RLlWPj9aU",
  'authDomain': "test-d1776.firebaseapp.com",
  'databaseURL': "https://test-d1776-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "test-d1776",
  'storageBucket': "test-d1776.appspot.com",
  'messagingSenderId': "475077380754",
  'appId': "1:475077380754:web:b30a5b819da6a4cb1a344b",
  'measurementId': "G-GRS8LTFV9B"
}

    
    
def getserial():
    try:
        f = open('/proc/cpuinfo',"r")
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close
    except:
        cpuserial = "ERROR000000000"
    return cpuserial



def recording_video(file_h264, file_mp4):
    camera = PiCamera()
    camera.start_recording(file_h264)
    sleep(5)
    camera.stop_recording()
    print(file_h264+" saved")
    try:
        command = "MP4Box -add " + file_h264 + " " + file_mp4
        call([command], shell = True)
    except Exception as e:
        print(e)
    camera.close()
    print(file_mp4.split()[-1]+" saved")
    remove_file(file_h264)
    return


def make_photo(name):
    camera = PiCamera()
    camera.capture(name)
    print(name+" saved")
    camera.close()
    return
    
def remove_file(name):
    os.remove(name)
    print("File "+ name+ " removed")
    return
    
def import_fierbase(folder,ID_device,name):
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    storage.child(folder).child(ID_device).child(name).put(name)
    print("Data sent to firebase storage")
    return
    
def Tvideo_Fphoto(type_data):
    ID_device = getserial()
    print("id device: "+ ID_device)
    dt = datetime.now().strftime("%Y-%m-%d_%H:%M")
    print("data: " +dt)
    print("pushed")
    if(type_data):
        name = dt+".mp4"
        save_path = "/home/pi/Desktop"
        completed_video = os.path.join(save_path, dt)
        recording_video(completed_video+".h264",completed_video+".mp4")
        folder = "Pill_Taking_Registration"
    else:
        name = dt+".jpg"
        make_photo(name)
        folder = "Picture_Pill_position"
    import_fierbase(folder,ID_device,name)
    remove_file(name)