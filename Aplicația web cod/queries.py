import data_manager


def add_position_patient(latitude, longitude, date, patient_id):
    data_manager.execute_insert(
        """INSERT INTO patient_locations VALUES ( DEFAULT, %(latitude)s, %(longitude)s,%(date)s,%(patient_id)s)""",
        {"patient_id": patient_id,
         'latitude': latitude,
         "longitude": longitude,
         "date": date})


def add_health_properties(patient_id, data_measure, EMG, EKG, body_composition=None, systolic_blood_pressure=None,
                          diastolic_blood_pressure=None, arterial_pressure=None, glucose=None, A1C=None, oxygen=None, temperature=None,
                          activity_calories=None):
    data_manager.execute_insert("""INSERT INTO health_properties 
    VALUES(DEFAULT,%(patient_id)s,%(data_measure)s,%(EMG)s,%(EKG)s,%(body_composition)s,
    %(systolic_blood_pressure)s,%(diastolic_blood_pressure)s,%(arterial_pressure)s,%(glucose)s,%(A1C)s,
    %(oxygen)s,%(temperature)s,%(activity_calories)s)""",
        {"patient_id": patient_id, "data_measure": data_measure,"EMG": EMG, "EKG": EKG,
         "body_composition": body_composition, "systolic_blood_pressure": systolic_blood_pressure,
         "diastolic_blood_pressure": diastolic_blood_pressure, "arterial_pressure": arterial_pressure,
         "glucose": glucose, "A1C": A1C, "oxygen": oxygen, "temperature": temperature, "activity_calories": activity_calories})


def get_all_patients():
    return data_manager.execute_select("""SELECT * FROM patient""")


def take_user_and_password(email):
    return data_manager.execute_select('''SELECT * FROM users WHERE email = %(email)s''', {'email': email})


def register_user(email, pass_encrypted):
    data_manager.execute_insert("""
                INSERT INTO users(email, password)
                VALUES(%(email)s, %(pass_encrypted)s)""",
        {"email": email,
        "pass_encrypted": pass_encrypted,})


def take_all_houses():
    return data_manager.execute_select('''SELECT * FROM housing''')


def take_all_patient_from_house(house_id):
    return data_manager.execute_select("""
        SELECT * FROM patient p
        INNER JOIN room r ON r.patient_id = p.id
        INNER JOIN housing h ON r.housing_id = h.id
        WHERE h.id = %(house_id)s
        """, {"house_id": house_id})


def take_room_from_house(house_id):
    return data_manager.execute_select("""SELECT * FROM room WHERE housing_id = %(house_id)s"""
                                       , {'house_id': house_id})


def take_house_detail(house_id):
    return data_manager.execute_select("""SELECT * FROM housing WHERE id = %(house_id)s """
                                    , {'house_id': house_id})


def get_patient_house(patient_id):
    return data_manager.execute_select("""
    SELECT * FROM housing h
    INNER JOIN room r ON h.id = r.housing_id
    INNER JOIN patient p ON p.id = r.patient_id
    WHERE p.id = %(patient_id)s""", {'patient_id': patient_id})


def get_patient_room(patient_id):
    return data_manager.execute_select("""SELECT * FROM room where patient_id = %(patient_id)s""",
                                       {"patient_id": patient_id})


def get_patient_legal_guardian(patient_id):
    return data_manager.execute_select("""SELECT * FROM legal_guardian where patient_id = %(patient_id)s"""
                                       , {"patient_id": patient_id})


def get_patient_treatment(patient_id):
    print(patient_id)
    return data_manager.execute_select("""SELECT * FROM patient_treatment where patient_id = %(patient_id)s"""
                                       , {"patient_id": patient_id})


def get_patient_condition(patient_id):
    return data_manager.execute_select("""SELECT * FROM patient_condition where patient_id = %(patient_id)s"""
                                       , {"patient_id": patient_id})


def get_patient(patient_id):
    return data_manager.execute_select("""SELECT * FROM patient where id = %(patient_id)s"""
                                       , {"patient_id": patient_id})


def get_patient_location(patient_id):
    return data_manager.execute_select("""
    SELECT * FROM patient_locations where patient_id = %(patient_id)s
    ORDER BY data_take_location DESC LIMIT 40""", {"patient_id": patient_id})


def check_taking_pills(patient_id):
    return data_manager.execute_select(
        """SELECT * FROM taking_pills where patient_id = %(patient_id)s""", {"patient_id": patient_id})


def check_error_pills(patient_id):
    return data_manager.execute_select(
        """SELECT * FROM fail_detection_pills where patient_id = %(patient_id)s""", {"patient_id": patient_id})


def get_patient_devices_associated_phone(phone_id):
    return data_manager.execute_select(
        """SELECT * FROM patient_devices WHERE phoneid = %(phone_id)s""", {'phone_id': phone_id})


def get_patient_devices_associated_camera(camera_id):
    return data_manager.execute_select(
        """SELECT * FROM patient_devices WHERE cameraid = %(camera_id)s""", {'camera_id': camera_id})


def add_recording_link(url, patient_id, data_taking):
    return data_manager.execute_insert(
        """INSERT INTO taking_pills VALUES (DEFAULT, %(data_taking)s,%(url)s,null,%(patient_id)s) """
        , {'data_taking': data_taking, 'url': url, 'patient_id': patient_id})


def add_image_link(url, patient_id, data_taking):
    return data_manager.execute_insert(
        """INSERT INTO fail_detection_pills VALUES (DEFAULT, %(data_taking)s,%(url)s,null,%(patient_id)s) """
        , {'data_taking': data_taking, 'url': url, 'patient_id': patient_id})


def add_house(residence_name, town, name_street, number_street, capacity, link_maps):
    return data_manager.execute_insert(
        """ INSERT INTO housing VALUES (DEFAULT, %(residence_name)s, %(town)s, %(name_street)s, %(number_street)s, 
        %(capacity)s, %(link_maps)s) """, {"residence_name": residence_name, "town": town, "name_street": name_street,
                                            "number_street": number_street, "capacity": capacity, "link_maps": link_maps})


def add_patient(first_name, last_name, cnp, phone, date_birth, religion):
    return data_manager.execute_insert("""
    INSERT INTO patient VALUES (DEFAULT,NULL,%(first_name)s,%(last_name)s,%(cnp)s,%(phone)s,%(date_birth)s,%(religion)s)""",
                                       {"first_name": first_name, "last_name": last_name, "cnp": cnp, "phone": phone,
                                        "date_birth": date_birth, "religion": religion})


def get_patient_id(cnp):
    return data_manager.execute_select("""SELECT id FROM patient where cnp = %(cnp)s"""
                                       , {"cnp": cnp})


def add_room(floor, room, comfort, patient_id, house_id):
    return data_manager.execute_insert("""
    INSERT INTO room VALUES (DEFAULT,%(floor)s,%(room)s,%(comfort)s,%(patient_id)s,%(house_id)s)""",
                                       {"floor": floor, "room": room, "comfort": comfort, "patient_id": patient_id,
                                        "house_id": house_id})


def add_guardian(first_name_guardian, last_name_guardian, phone_guardian, patient_id):
    return data_manager.execute_insert("""
        INSERT INTO legal_guardian VALUES (DEFAULT,%(first_name_guardian)s,%(last_name_guardian)s,%(phone_guardian)s,%(patient_id)s)""",
                                       {"first_name_guardian": first_name_guardian, "last_name_guardian": last_name_guardian,
                                        "phone_guardian": phone_guardian, "patient_id": patient_id})


def add_device(patient_id, phone_id, camera_id):
    return data_manager.execute_insert("""
            INSERT INTO patient_devices VALUES (DEFAULT,%(patient_id)s,%(phone_id)s,%(camera_id)s)""",
                                       {"patient_id": patient_id, "phone_id": phone_id, "camera_id": camera_id})


def add_condition_patient(disease, manifestation, unexpected_events, limitation, patient_id):
    return data_manager.execute_insert("""
        INSERT INTO patient_condition VALUES (DEFAULT,%(disease)s,%(manifestation)s,%(unexpected_events)s,%(limitation)s,%(patient_id)s)""",
                                       {"disease": disease, "manifestation": manifestation,
                                        "unexpected_events": unexpected_events, "limitation": limitation,
                                        "patient_id": patient_id})


def add_treatment_patient(medical_supplies, recommended_activity, perimeter, patient_id):
    return data_manager.execute_insert("""
                INSERT INTO patient_treatment VALUES(DEFAULT,%(medical_supplies)s,%(recommended_activity)s,%(perimeter)s,%(patient_id)s)""",
                                       {"medical_supplies": medical_supplies,
                                        "recommended_activity": recommended_activity, "perimeter": perimeter,
                                        "patient_id": patient_id})


def update_patient(url, patient_id):
    return data_manager.execute_insert("""
    UPDATE patient SET image = %(url)s WHERE id=%(patient_id)s""", {"url": url, "patient_id": patient_id})


def edit_error_pills(patient_id, validation):
    return data_manager.execute_insert("""
        UPDATE fail_detection_pills SET problem_solved = %(validation)s WHERE id=%(patient_id)s""",
                                       {"validation": validation, "patient_id": patient_id})


def edit_taking_pills(patient_id, validation):
    return data_manager.execute_insert("""
            UPDATE taking_pills SET has_took_pill = %(validation)s WHERE id=%(patient_id)s""",
                                       {"validation": validation, "patient_id": patient_id})


def add_patient_health_properties(patient_id, data, weight, systolic, diastolic, arterial, glucose, A1C, oxygen,
                                  temperature, activity):
    return data_manager.execute_insert("""
                INSERT INTO health_properties VALUES(DEFAULT,%(patient_id)s,%(data)s,NULL, NULL,%(weight)s,%(systolic)s,
                %(diastolic)s,%(arterial)s,%(glucose)s,%(A1C)s,%(oxygen)s,%(temperature)s,%(activity)s)""",
                                       {"patient_id": patient_id, "data": data, "weight": weight, "systolic": systolic,
                                        "diastolic": diastolic, "arterial": arterial, "glucose": glucose, "A1C": A1C,
                                        "oxygen": oxygen, "temperature": temperature, "activity": activity})


def get_patient_health_properties(patient_id):
    return data_manager.execute_select("""
    SELECT * FROM health_properties where patient_id = %(patient_id)s
    ORDER BY data_measure DESC LIMIT 40""", {"patient_id": patient_id})


def add_question(patient_id, data, question):
    return data_manager.execute_insert("""
    INSERT INTO patient_questions VALUES (DEFAULT, %(patient_id)s, %(data)s, %(question)s, NULL)""",
    {"patient_id": patient_id, "data": data, "question": question})