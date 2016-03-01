# encoding: utf-8

import os

#### Ici il me reste beaucoup à faire et à apprendre comment faire....
#### Mais la récuperation par la methode Export fonctionne bien.

SETUP = """

RECTS = %s

import os,time
#import RPi.GPIO as GPIO

##### SET MODE #####

#GPIO.setmode(GPIO.BOARD)

##### SET CHANNEL #####

inputPin = []
outputPin = [rec[1] / rec[3] -1 for rec in RECTS]      ## recupere la clef TrackNUm du dictionnaire
print outputPin

#GPIO.setup(inputPin, GPIO.IN)
#GPIO.setup(outputPin, GPIO.OUT)
"""
SEQUENCE = """    
def blink(pin,i):

    start = RECTS[i][0] * 0.01
    width = RECTS[i][2] * 0.01
    print start                    # RECT_START
    time.sleep(start)              # start time
    #GPIO.output(pin, 1)
    print "on", width
    time.sleep(width)              # width time
    #GPIO.output(pin,0)
    print "off"

for i in range(len(outputPin)):
    pin = outputPin[i]
    blink(pin,i)

#GPIO.cleanup()
"""