# encoding: utf-8

import os

SETUP = """

dictGPIO = %s

import os,time
from multiprocessing import Process
import RPi.GPIO as GPIO

##### SET MODE #####
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

##### SET CHANNEL #####
inputPin = []
outputPin =dictGPIO.keys()
print outputPin

#GPIO.setup(inputPin, GPIO.IN)
GPIO.setup(outputPin, GPIO.OUT)
GPIO.output(outputPin, 0)
"""
SEQUENCE = """    
def blink(pin):
    for i in range(len(dictGPIO[pin]["RECT_START"])):
        if i == 0:
            start = dictGPIO[pin]["RECT_START"][i] * 0.1
            width = dictGPIO[pin]["RECT_WIDTH"][i] * 0.1
            print "pin %d StandBy" % pin, start, time.time()
            time.sleep(start)              # start time
            GPIO.output(pin, 1)
            print "pin %d 'ON' for %0f sec" % (pin,width), time.time()
            time.sleep(width)              # width time
            GPIO.output(pin, 0)
            print "pin %d off" % pin, time.time()
        else:
            start = (dictGPIO[pin]["RECT_START"][i] - dictGPIO[pin]["RECT_STOP"][i-1]) * 0.1
            width = dictGPIO[pin]["RECT_WIDTH"][i] * 0.1
            print "pin %d StandBy" % pin, start, time.time()
            time.sleep(start)              # start time
            GPIO.output(pin, 1)
            print "pin %d 'ON' for %0f sec" % (pin,width), time.time()
            time.sleep(width)              # width time
            GPIO.output(pin, 0)
            print "pin %d off" % pin, time.time()
    
PROCESS = []
print "loop process begins"

for i in range(len(outputPin)):
    pin = outputPin[i]
    process = Process(target=blink, args=(pin,))
    PROCESS.append(process)
    process.start()
    print "process.start()"
    
print "Process liste", PROCESS

for p in PROCESS:
    p.join()
    print "process.join()"
    
GPIO.cleanup()
print "CLEANUP!!"
"""