
import RPi.GPIO as GPIO
from time import sleep
import os
import sys

#Defaults that we are using GPIO pins and Turns off warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pins used on GPIO Raspberry Pi Board
lightPin = 4        
buttonPin = 17

GPIO.setup(lightPin, GPIO.OUT) #light pin will be an OUTPUT to make it light up
GPIO.setup(buttonPin, GPIO.IN, pull_up_down= GPIO.PUD_UP) #button takes user INPUT
GPIO.output(lightPin, False)    #sets LED light off

#Runs script if button is pressed
def button_callback(buttonPin):
    os.system("python /home/pi/Desktop/PhotoDownloader.py")
    GPIO.output(lightPin, False)
    print('Press Button to Start')

#watches and waits for button to be pressed
GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback, bouncetime = 60000)

print('Press Button To Start')

#keeps looping until button has been pressed
try:
    while True:
        if GPIO.event_detected(buttonPin):
            GPIO.output(lightPin, True)          
        sleep(0.0001)


#Clean Up GPIO when program closes
finally:
    print('Cleaning up')
    GPIO.cleanup() 
