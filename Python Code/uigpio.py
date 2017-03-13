#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv/
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

# GPIO 23 set up as input. It is pulled up to stop false signals
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button23(self):
    print('get next picture')
    print('draw next screen')    


def button24(self):
    print('get previous picture')
    print('draw previous screen')    


#def doButtons():
#    if GPIO.event_detected(23):
#    if GPIO.event_detected(24):


GPIO.add_event_detect(23, GPIO.FALLING, callback=button23, bouncetime=200)  # add rising edge detection on a channel
GPIO.add_event_detect(24, GPIO.FALLING, callback=button24, bouncetime=200)  # add rising edge detection on a channel

#GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)  

while True:
    try:
        #doButtons()
        sleep(0.1)
        #print("First instruction")

    except KeyboardInterrupt:
        GPIO.cleanup()
    
