


import RPi.GPIO as GPIO  
import time



pin_no = 11

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  

# set up GPIO output channel  
GPIO.setup(pin_no, GPIO.OUT)  

GPIO.output(pin_no,GPIO.LOW)

time.sleep(500)

GPIO.cleanup() 



