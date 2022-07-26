import time
import firebase_test
from threading import Timer

import RPi.GPIO as GPIO

TRIG = 22
ECHO = 24
can_pass_photo = True
can_pass_video = True

def ultrasonic_initialization():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, False)
        time.sleep(2)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            pulse_start= time.time()
        while GPIO.input(ECHO)==1:
            pulse_end= time.time()
        pulse_duration= pulse_end - pulse_start
        distance= pulse_duration * 17150
        distance= round(distance,2)
        print( "Distance: ",distance," cm")
        GPIO.cleanup()
        return distance

def is_time_up_photo():
    global can_pass_photo
    can_pass_photo = True
    
def is_time_up_video():
    global can_pass_video
    can_pass_video = True
    

def main():
    global can_pass_photo
    global can_pass_video
    while True:
        try:
            distance = ultrasonic_initialization()
            if(distance > 9):
                if(can_pass_video):
                    can_pass_video = False
                    Timer(60.0*60.0*3.0,is_time_up_video).start()
                    firebase_test.Tvideo_Fphoto(True)
                elif(can_pass_photo):
                    can_pass_photo = False
                    Timer(60.0*30.0,is_time_up_photo).start()
                    firebase_test.Tvideo_Fphoto(False)
            time.sleep(3)
        except:
            print("error")
            time.sleep(3)


if __name__ == '__main__':
    main()
