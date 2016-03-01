# encoding: utf-8

import os

#### Ici il me reste beaucoup à faire et à apprendre comment faire....
#### Mais la récuperation par la methode Export fonctionne bien.

SETUP = """

dictGPIO = %s

import os,time
#import RPi.GPIO as GPIO

##### SET MODE #####

#GPIO.setmode(GPIO.BOARD)

##### SET CHANNEL #####

inputPin = []
outputPin = dictGPIO.keys()      ## recupere la clef TrackNUm du dictionnaire

#GPIO.setup(inputPin, GPIO.IN)
#GPIO.setup(outputPin, GPIO.OUT)
"""
SEQUENCE = """    
def blink(pin):
    RECT_START = dictGPIO[pin]["RECT_START"]     
    RECT_WIDTH = dictGPIO[pin]["RECT_WIDTH"]
    for x in RECT_START:
        i = RECT_START.index(x) 
        ts = x * 0.01 
        tw = RECT_WIDTH[i] * 0.01
        print ts                    # RECT_START
        time.sleep(ts)              # start time
        #GPIO.output(pin, 1)
        print "on", tw
        time.sleep(tw)              # width time
        #GPIO.output(pin,0)
        print "off"



for pin in outputPin:
    blink(pin)

#GPIO.cleanup()

"""