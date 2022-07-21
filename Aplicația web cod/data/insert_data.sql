INSERT INTO patient VALUES (DEFAULT,'https://firebasestorage.googleapis.com/v0/b/patient-supervision.appspot.com/o/Profile_Picture%2F1.jpeg?alt=media&token=b1de8f6c-6bae-447f-8fa0-5b0bdc08bc2c' ,'Ichimas','Marius-Cristian','5000430044338','0771057455','2000-04-30','Ortodox');
INSERT INTO patient VALUES (DEFAULT,'https://firebasestorage.googleapis.com/v0/b/test-d1776.appspot.com/o/Profile_Picture%2Fimage%2F2.jpg?alt=media&token=69adfc2a-87ac-4936-86c7-fb4d4ded62a4' ,'Maria','Elena','5000443041258','0771057451','2000-04-30','Ortodox');
INSERT INTO patient VALUES (DEFAULT,'https://console.firebase.google.com/u/0/project/test-d1776/storage/test-d1776.appspot.com/files/~2FProfile_Picture~2Fimage' ,'Stan','Lee','5000430044331','0771057454','2001-07-10','Ortodox');
INSERT INTO patient VALUES (DEFAULT,'https://firebasestorage.googleapis.com/v0/b/test-d1776.appspot.com/o/Profile_Picture%2Fimage%2F4.jpg?alt=media&token=3677715a-544a-4a80-be1e-f2235d11e8dc' ,'Gheorghe','Marian','5000432044332','0771057456','2006-05-10','');


INSERT INTO patient_devices VALUES  (DEFAULT,1,'9fc671cbb943632a','00000000573b99b7');
INSERT INTO patient_devices VALUES  (DEFAULT,2,'9fc671cbb9436366','00000000573b9977');
INSERT INTO patient_devices VALUES  (DEFAULT,3,'9fc671cbb9436377','00000000573b9988');
INSERT INTO patient_devices VALUES  (DEFAULT,4,'9fc671cbb9436388','00000000573b9999');

INSERT INTO legal_guardian VALUES (DEFAULT,'Ichimas','Elena','0774025315',1);
INSERT INTO legal_guardian VALUES (DEFAULT,'Vitan','Vasile','0774025315',2);
INSERT INTO legal_guardian VALUES (DEFAULT,'Stan','Elena','0774025315',3);
INSERT INTO legal_guardian VALUES (DEFAULT,'Marian','Emanoil','0774025315',4);

INSERT INTO housing Values (DEFAULT,'Camin Leu','Bucharest','Iuliu-Maniu',3,8,'https://www.google.com/maps/place/C%C4%83min+Leu+A/@44.4340961,26.0530881,17z/data=!3m1!4b1!4m5!3m4!1s0x40b201db2e1c6995:0x6ed521e82cb68d45!8m2!3d44.4341303!4d26.0553024');
INSERT INTO housing Values (DEFAULT,'Emaus','Brasov','Iurdan',1,3,'https://www.google.com/maps/place/C%C4%83min+Leu+A/@44.4340961,26.0530881,17z/data=!3m1!4b1!4m5!3m4!1s0x40b201db2e1c6995:0x6ed521e82cb68d45!8m2!3d44.4341303!4d26.0553024');
INSERT INTO housing Values (DEFAULT,'Leului','Sibiu','Tragediei',3,4,'https://www.google.com/maps/place/C%C4%83min+Leu+A/@44.4340961,26.0530881,17z/data=!3m1!4b1!4m5!3m4!1s0x40b201db2e1c6995:0x6ed521e82cb68d45!8m2!3d44.4341303!4d26.0553024');
INSERT INTO housing Values (DEFAULT,'Emanoil house','Comanesti','Doinei',1,1,'https://www.google.com/maps/place/C%C4%83min+Leu+A/@44.4340961,26.0530881,17z/data=!3m1!4b1!4m5!3m4!1s0x40b201db2e1c6995:0x6ed521e82cb68d45!8m2!3d44.4341303!4d26.0553024');


INSERT INTO patient_condition VALUES (DEFAULT,'cancer','scuipa sange',null,null,1);
INSERT INTO patient_condition VALUES (DEFAULT,'Abazie','furie',null,null,2);
INSERT INTO patient_condition VALUES (DEFAULT,'Absintism','ameteli',null,null,3);
INSERT INTO patient_condition VALUES (DEFAULT,'Boala Bornholm, COVID-19','tuse, dureri musculare',null,null,4);



INSERT INTO patient_treatment VALUES (DEFAULT,'paracetamol','plimbare cu cainele',30,1);
INSERT INTO patient_treatment VALUES (DEFAULT,'avocalmin','30 minute intinsa',60,2);
INSERT INTO patient_treatment VALUES (DEFAULT,'Ciclizină','expunerea la soare ziua',0,3);
INSERT INTO patient_treatment VALUES (DEFAULT,'Fluoxetină','calarit',0,4);

INSERT INTO room VALUES (DEFAULT,1,5,1,1,1);
INSERT INTO room VALUES (DEFAULT,3,4,4,2,2);
INSERT INTO room VALUES (DEFAULT,4,14,1,3,3);
INSERT INTO room VALUES (DEFAULT,10,2,4,4,4);

INSERT INTO users VALUES ('cry_ichimas@yahoo.com','$2b$12$kzXyyDsVvpdK3dtetQ/gBOkbGo9Rjb1vV4G6l/YtrVKcwGILOumDi');

