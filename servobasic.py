import RPi.GPIO as GPI
import time
import math
GPI.setmode(GPI.BOARD)
GPI.setup(12,GPI.OUT)
p2= GPI.PWM(12, 50)
p2.start(2.5)
#p2.ChangeDutyCycle(4.5)
#time.sleep(2)
def rotate_arm(x, y):
    #m=(y-225)/(x-320)
    
    #print(m)
    deg=math.degrees(math.atan(y/x))
    #deg=math.degrees(math.atan(m))
    #adj=(x-18)/math.atan(m)
    #print(deg)
    #print(adj)
    #n=x/adj
    #deg1=math.atan2(x/adj)
    #print(n)
    #deg1=math.degrees(math.atan(n))
    #print(deg1)
    dutycycle = (deg/ 18) + 2
    #print(dutycycle)
    p2.ChangeDutyCycle(dutycycle)
    time.sleep(2)

rotate_arm(100,200)