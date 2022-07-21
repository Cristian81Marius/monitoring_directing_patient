import pyrebase
import os
import queries

filelist = [f for f in os.listdir(".") if f.endswith(".JPG")]
for f in filelist:
    os.remove(os.path.join(".", f))

firebaseConfig = {
  'apiKey': "AIzaSyAyGwesvzexk9GkSziuUoUnm5RLlWPj9aU",
  'authDomain': "test-d1776.firebaseapp.com",
  'databaseURL': "https://test-d1776-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "test-d1776",
  'storageBucket': "test-d1776.appspot.com",
  'messagingSenderId': "475077380754",
  'appId': "1:475077380754:web:b30a5b819da6a4cb1a344b",
  'measurementId': "G-GRS8LTFV9B",
  'serviceAccount': "serviceAccountKeytTest.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()


def add_data_real_time():
    while True:
        existent_data = db.get()
        if existent_data.val() is not None:
            for existent_data in existent_data.each():
                phone_id = existent_data.key()
                try:
                    patient_id = queries.get_patient_devices_associated_phone(phone_id)[0]["patient_id"]
                    add_data_inserted_phone(phone_id, patient_id)
                except:
                    print("we dont have this device")


def add_data_inserted_phone(phone_id, patient_id):
        emg = db.child(phone_id).child("EMG").get()
        ekg = db.child(phone_id).child("EKG").get()
        fqa = db.child(phone_id).child("FQA").get()
        location = db.child(phone_id).child("Location").get()
        if fqa.val() is not None:
            for fqa in fqa.each():
                fqa_property = fqa.val()["MyProperty"]
                try:
                    queries.add_question(patient_id, fqa_property["DataTime"], fqa_property["ValueFQA"])
                except(ValueError):
                    print("is not valid number")
            db.child(phone_id).child("FQA").remove()
        if emg.val() is not None:
            for emg in emg.each():
                emg_property = emg.val()["MyProperty"]
                try:
                    queries.add_health_properties(patient_id, emg_property["DataTime"], float(emg_property["ValueEMG"].replace(",", ".")), None)
                except(ValueError):
                    print("is not valid number")
            db.child(phone_id).child("EMG").remove()
        if ekg.val() is not None:
            for ekg in ekg.each():
                ekg_property = ekg.val()["MyProperty"]
                try:
                    queries.add_health_properties(patient_id, ekg_property["DataTime"], None, float(ekg_property["ValueEKG"].replace(",", ".")))
                except(ValueError):
                    print("is not valid number")
            db.child(phone_id).child("EKG").remove()
        if location.val() is not None:
            for location in location.each():
                location_property = location.val()["MyProperty"]
                try:
                    print("b")
                    queries.add_position_patient(float(location_property["Latitude"].replace(",", "."))
                                                  ,float(location_property["Longitude"].replace(",", "."))
                                                  ,location_property["DataTime"], patient_id)
                except:
                    continue
                finally:
                    db.child(phone_id).child("Location").child(location.key()).remove()


def take_data_storage():
    while True:
        all_files = storage.list_files()
        for file in all_files:
            elements = file.name.split("/")
            if (elements[-1] != '') and (elements[0] != "Profile_Picture"):
                patient_id = queries.get_patient_devices_associated_camera(elements[1])[0]["patient_id"]
                url = storage.child(elements[0]).child(elements[1]).child(elements[2]).get_url(None)
                data_taking = elements[2].split(".")[0].replace("_", " ")
                if elements[0] == "Pill_Taking_Registration":
                    try:
                        queries.add_recording_link(url, patient_id, data_taking)
                    except:
                        continue
                elif elements[0] == "Picture_Pill_position":
                    try:
                        queries.add_image_link(url, patient_id, data_taking)
                    except:
                        continue


def save_patient_picture(image):
    storage.child("Profile_Picture").child(image).put(image)
    url = storage.child("Profile_Picture").child(image).get_url(None)
    return url

