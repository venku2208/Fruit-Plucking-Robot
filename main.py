from picamera.array import PiRGBArray
from picamera import PiCamera
import sys
import RPi.GPIO as GPIO
import time
import os
import cv2
import imutils
import math
from stepperbasic import stepfor



redLower = (0, 100, 100)
redUpper = (20, 255, 255)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(37,GPIO.OUT)
p3= GPIO.PWM(37, 50)
GPIO.setup(12,GPIO.OUT)
p2= GPIO.PWM(12, 50)




def positionServo (servo, angle):
    os.system("python miniservo.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))
def mapServoPosition (x,y):
     
       
         for i in range(x!=0): 
             p2.start(2.5)
             p3.start(2.5)
                         
             deg=math.degrees(math.atan(x/y))
             dutycycle = (deg/25) + 2.0
             print(deg)
             p2.ChangeDutyCycle(dutycycle)
             time.sleep(2)
             from stepperbasic import stepfor
             stepfor()
             time.sleep(2)
             p3.start(2.5)
             p3.ChangeDutyCycle(2.5)
             time.sleep(4)
             p3.ChangeDutyCycle(6.5)
             time.sleep(4)
             from stepperbasic import stepback
             stepback()
             p2.ChangeDutyCycle(4.0)
             time.sleep(2)
             
             p2.ChangeDutyCycle(3.0)
             time.sleep(2)
            
             p3.ChangeDutyCycle(2.5)
             time.sleep(2)
             p3.ChangeDutyCycle(10.5)
             time.sleep(2)

             
             exit()
             
          
             




# allow the camera or video file to warm up
time.sleep(1.0)

#function to get reliable coordinates from set
def get_best_coordinate(l):
    x_list = []
    for each in l:
        inserted = False
        for e in x_list:
            for i in e:
                if(each-i<=20 and each-i>=-20):
                    e.append(each)
                    inserted = True
                    break
        if(not inserted):
            x_list.append([each])
    #find set with lexographically greater length
    g_len = 0
    set = []
    for each in x_list:
        if(len(each))>g_len:
            set = each
    val = sum(set)/len(set)
    return val
    

# initialize the camera and grab a reference to the raw camera capture
def Cam():
    global x
    global i
    i = 0
    camera = PiCamera()
    camera.resolution = (640,480)
    rawCapture = PiRGBArray(camera,size=(640,480))
    x,y = None,None
     
    # allow the camera to warmup
    time.sleep(0.1)
    x_coordinates = []
    y_coordinates = []
    while True:
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        frame = imutils.resize(image, width=600)
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, redLower, redUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
    
        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                x_coordinates.append(x)
                y_coordinates.append(y)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                print('object found with x:{} y:{}'.format(x,y))
                
                # only proceed if the radius meets a minimum size
                if radius >10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)

        cv2.imwrite('image.jpg',frame)           
        rawCapture.truncate(0)
        if x!=None and y!=None and i==5:
            mapServoPosition(x,y)
            
            break
        i+=1
    x_val = get_best_coordinate(x_coordinates)
    y_val = get_best_coordinate(y_coordinates)
    #sb.rotate_arm(60, ((450-y_val)/9)-13)
    
    sb.rotate_arm((x_val-40),y_val)
        
                         
Cam()