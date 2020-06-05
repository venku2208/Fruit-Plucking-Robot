
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
StepPins=[18,22,24,26]
for pin in StepPins:
    GPIO.setup(StepPins,GPIO.OUT)
    GPIO.output(pin,0) 
Seq=[[1,0,0,0],
     [1,1,0,0],
     [0,1,0,0],
     [0,1,1,0],
     [0,0,1,0],
     [0,0,1,1],
     [0,0,0,1],
     [1,0,0,1]]

Seq2=[[1,0,0,1],
     [0,0,0,1],
     [0,0,1,1],
     [0,0,1,0],
     [0,1,1,0],
     [0,1,0,0],
     [1,1,0,0],
     [1,0,0,0]]

for i in range(0):
    for Seq1 in range(8):
        for pin in range(4):
           GPIO.output(StepPins[pin],Seq2[Seq1][pin])
        time.sleep(0.001)
for i in range(1500):
    for Seq1 in range(8):
        for pin in range(4):
           GPIO.output(StepPins[pin],Seq[Seq1][pin])
        time.sleep(0.001)

GPIO.cleanup()