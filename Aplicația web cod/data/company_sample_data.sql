DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS housing CASCADE;
DROP TABLE IF EXISTS patient_questions CASCADE;
DROP TABLE IF EXISTS fail_detection_pills CASCADE;
DROP TABLE IF EXISTS health_properties CASCADE ;
DROP TABLE IF EXISTS patient_devices CASCADE;
DROP TABLE IF EXISTS patient_treatment CASCADE;
DROP TABLE IF EXISTS patient_locations CASCADE;
DROP TABLE IF EXISTS legal_guardian CASCADE;
DROP TABLE IF EXISTS taking_pills CASCADE;
DROP TABLE IF EXISTS patient_condition CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
DROP TABLE IF EXISTS users CASCADE ;


CREATE TABLE users(
    email text,
    password text
);

create table patient
(
    id            SERIAL      primary key,
    image         varchar,
    first_name    varchar(30) not null,
    last_name     varchar(30) not null,
    cnp           varchar(13) not null unique,
    phone         varchar(10),
    date_of_birth date,
    religion      varchar(15)
);


create table housing
(
    id            SERIAL      primary key,
    name        varchar,
    town          varchar not null,
    street        varchar not null,
    number_street integer,
    capacity      integer,
    link_maps   VARCHAR
);


create table patient_treatment
(
    id                            SERIAL      primary key,
    medical_supplies              varchar,
    recommended_activities        varchar,
    travel_perimeter              integer,
    patient_id                    integer not null

);

alter table only patient_treatment
    ADD constraint fk_treatment_patients_id FOREIGN KEY (patient_id)references patient(id);

create table patient_condition
(
    id                     SERIAL     primary key,
    disease                varchar,
    patient_manifestations varchar,
    unexpected_events      varchar,
    limitation             varchar,
    patient_id             integer not null
);

alter table only patient_condition
    ADD constraint fk_condition_patients_id FOREIGN KEY (patient_id)references patient(id);



create table legal_guardian
(
    id         SERIAL     primary key,
    first_name varchar(30) not null,
    last_name  varchar(30) not null,
    phone      varchar(10),
    patient_id integer     not null
);

alter table only legal_guardian
    ADD constraint fk_legal_guardian_patients_id FOREIGN KEY (patient_id)references patient(id);


create table room
(
    id          SERIAL        primary key,
    floor       smallint,
    number_room integer,
    comfort     smallint,
    patient_id  integer not null,
    housing_id  integer not null

);

alter table only room
    ADD constraint fk_room_patients_id FOREIGN KEY (patient_id)references patient(id);
alter table only room
    ADD constraint fk_room_housing_id FOREIGN KEY (housing_id)references housing(id);


create table patient_locations
(
    id                 SERIAL     primary key,
    longitude          double precision,
    latitude           double precision,
    data_take_location TIMESTAMP unique,
    patient_id         integer not null
);

alter table only patient_locations
    ADD constraint fk_patient_locations_patients_id FOREIGN KEY (patient_id)references patient(id);


create table taking_pills
(
    id          SERIAL        primary key,
    data_taking TIMESTAMP ,
    recorded    varchar unique ,
    has_took_pill bool,
    patient_id  integer not null
);

alter table only taking_pills
    ADD constraint fk_taking_pills_patients_id FOREIGN KEY (patient_id)references patient(id);


create table patient_devices
(
    id          SERIAL        primary key,
    patient_id  integer not null,
    phoneId     varchar,
    cameraId    varchar
);
alter table only patient_devices
    ADD constraint fk_devices_patients_id FOREIGN KEY (patient_id)references patient(id);


CREATE TABLE health_properties
(
    id      SERIAL      primary key ,
    patient_id  integer not null,
    data_measure timestamp,
    EMG float,
    EKG float,
    body_composition float,
    systolic_blood_pressure float,
    diastolic_blood_pressure float,
    arterial_pressure float,
    glucose float,
    A1C float,
    oxygen float,
    temperature float,
    activity_calories float
);
alter table only health_properties
    ADD constraint fk_health_patients_id FOREIGN KEY (patient_id)references patient(id);

CREATE TABLE fail_detection_pills
(
    id          SERIAL        primary key,
    data_taking TIMESTAMP ,
    image    varchar unique ,
    problem_solved bool,
    patient_id  integer not null
);

alter table only fail_detection_pills
    ADD constraint fk_dail_detect_patients_id FOREIGN KEY (patient_id)references patient(id);

CREATE TABLE  patient_questions(
    id  SERIAL primary key ,
    patient_id  INTEGER not null ,
    data_send date,
    question varchar,
    answer varchar
);

alter table only patient_questions
    ADD constraint fk_question_patients_id FOREIGN KEY (patient_id)references patient(id);