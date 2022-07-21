from flask import Flask, render_template, url_for, session, request,redirect
from dotenv import load_dotenv
import mimetypes
from threading import Timer
import os
import datetime

import hash_passord
import firebase_manipulation
import queries



mimetypes.add_type('application/javascript', '.js')
app = Flask(__name__)
load_dotenv()
app.secret_key = 'track_patients'
app.config["UPLOAD_FOLDER"] = os.path.join('image')


@app.route('/test')
def test():
    return "test"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user_name']
        password = request.form['password']
        if ((user in queries.take_user_and_password(user)[0]['email']) and
                hash_passord.verify_password(password, queries.take_user_and_password(user)[0]['password'])):
            session['user'] = user
            return redirect('/')
    else:
        if 'user' in session:
            return redirect('/')
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        pass_encrypted = hash_passord.hash_password(password)
        queries.register_user(email, pass_encrypted)
        session['user'] = email
        return redirect('/')
    return render_template('register.html')


@app.route('/house/<house_id>', methods=["GET", "POST"])
def patients_from_house(house_id):
    patients = queries.take_all_patient_from_house(house_id)
    rooms = queries.take_room_from_house(house_id)
    house = queries.take_house_detail(house_id)[0]
    return render_template('patients_from_house.html', patients=patients, rooms=rooms, house=house)


@app.route('/profile/patient/<patient_id>', methods=["GET", "POST"])
def patient_profile(patient_id):
    patient = queries.get_patient(patient_id)[0]
    condition = queries.get_patient_condition(patient_id)[0]
    treatment = queries.get_patient_treatment(patient_id)[0]
    legal_guardian = queries.get_patient_legal_guardian(patient_id)[0]
    room = queries.get_patient_room(patient_id)[0]
    house = queries.get_patient_house(patient_id)[0]
    return render_template("profile_patient.html", patient=patient, condition=condition, treatment=treatment,
                           legal_guardian=legal_guardian, room=room, house=house)


@app.route('/list/patients', methods=["GET", "POST"])
def all_patients():
    patients = queries.get_all_patients()
    return render_template("list_patients.html", patients=patients)


@app.route('/list/houses', methods=["GET", "POST"])
def all_houses():
    houses = queries.take_all_houses()
    return render_template('list_houses.html', houses=houses)


@app.route('/check_pills_patient/<patient_id>', methods=["GET", "POST"])
def take_pills(patient_id):
    records = queries.check_taking_pills(patient_id)
    images = queries.check_error_pills(patient_id)
    return render_template('validate_take_pills.html', records=records, images=images,
                           images_len=len(images), records_len=len(records), patient_id=patient_id)


@app.route('/edit/validate/image/<patient_id>', methods=["GET", "POST"])
def edit_validate_image(patient_id):
    validation = request.form["validate_image"]
    queries.edit_error_pills(patient_id, validation)
    return redirect(f'/check_pills_patient/{patient_id}')


@app.route('/edit/validate/video/<patient_id>', methods=["GET", "POST"])
def edit_validate_video(patient_id):
    validation = request.form["validate_video"]
    queries.edit_taking_pills(patient_id, validation)
    return redirect(f'/check_pills_patient/{patient_id}')


@app.route("/add/house", methods=["GET", "POST"])
def new_house():
    return render_template('add_new_house.html')


@app.route("/add/new/house", methods=["GET", "POST"])
def import_database_house():
    residence_name = request.form['residence_name']
    town = request.form['town']
    name_street = request.form['street']
    number_street = request.form['number']
    capacity = request.form['capacity']
    maps_link = request.form["link_maps"]
    queries.add_house(residence_name, town, name_street, number_street, capacity, maps_link)
    return redirect("/list/houses")


@app.route("/add/patient", methods=["GET", "POST"])
def new_patient():
    houses = queries.take_all_houses()
    return render_template('add_new_patient.html', houses=houses)


@app.route("/add/new/patient", methods=["GET", "POST"])
def import_database_patient():
    # personal data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    cnp = request.form['cnp']
    phone = request.form['phone']
    date_birth = request.form['date_birth']
    religion = request.form["religion"]
    queries.add_patient(first_name, last_name, cnp, phone, date_birth, religion)
    patient_id = queries.get_patient_id(cnp)[0]["id"]
    #save image
    image = request.files["patient_image"]
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{patient_id}.jpg"))
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{patient_id}.png')
    url = firebase_manipulation.save_patient_picture(f"image/{patient_id}.jpg")
    queries.update_patient(url, patient_id)

    # room
    house_id = int(request.form['house_id'])
    room = int(request.form["room"])
    floor = int(request.form["floor"])
    comfort = int(request.form["comfort"])
    queries.add_room(floor, room, comfort, patient_id, house_id)
    # guardian
    first_name_guardian = request.form["first_name_guardian"]
    last_name_guardian = request.form["last_name_guardian"]
    phone_guardian = request.form["phone_guardian"]
    queries.add_guardian(first_name_guardian, last_name_guardian, phone_guardian, patient_id)
    # devices
    phone_id = request.form["phone_id"]
    camera_id = request.form["camera_id"]
    queries.add_device(patient_id, phone_id, camera_id)
    # condition
    disease = request.form["disease"]
    manifestation = request.form["manifestation"]
    unexpected_events = request.form["unexpected_events"]
    limitation = request.form["limitation"]
    queries.add_condition_patient(disease, manifestation, unexpected_events, limitation, patient_id)
    # treatment
    medical_supplies = request.form["medical_supplies"]
    recommended_activity = request.form["recommended_activity"]
    perimeter = request.form["perimeter"]
    queries.add_treatment_patient(medical_supplies, recommended_activity, perimeter, patient_id)
    return redirect("/list/patients")


@app.route('/add/patient/health/property/<patient_id>', methods=["GET", "POST"])
def add_patient_data_smartwatch(patient_id):
    weight = request.form['Weight']
    systolic = request.form['Systolic']
    diastolic = request.form['Diastolic']
    arterial = request.form['Arterial']
    glucose = request.form['Glucose']
    A1C = request.form['A1C']
    oxygen = request.form['Oxygen']
    if oxygen == '': oxygen = None
    temperature = request.form['Temperature']
    if temperature == '': temperature = None
    activity = request.form['Activity']
    if activity == '': activity = None
    queries.add_patient_health_properties(patient_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), weight,
                                          systolic, diastolic, arterial, glucose, A1C, oxygen, temperature, activity)
    return redirect(f'/show/patient/health/property/{patient_id}')


@app.route('/add/new/health/property/<patient_id>', methods=["GET", "POST"])
def new_health_property(patient_id):
    return render_template('add_patient_health_property.html', patient_id=patient_id)


@app.route('/show/patient/health/property/<patient_id>', methods=["GET", "POST"])
def health_properties(patient_id):
    watch_data = queries.get_patient_health_properties(patient_id)
    phone_data = queries.get_patient_location(patient_id)
    return render_template('patient_health_property.html', watch_data=watch_data, phone_data=phone_data,
                           patient_id=patient_id)


@app.route('/')
def index():
    return render_template('index.html')


def main():
    app.run(debug=True)
    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))


if __name__ == '__main__':
    Timer(3.0, firebase_manipulation.add_data_real_time).start()
    Timer(5.0, firebase_manipulation.take_data_storage).start()
    main()

