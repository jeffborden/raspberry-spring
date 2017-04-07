import RPi.GPIO as GPIO
import time



class RaspberryLight:
    def __init__(self, pin_num):
        self.pin_num = pin_num

        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BOARD)

        # set up GPIO output channel
        GPIO.setup(pin_num, GPIO.OUT)

        # indicate setup to user
        self.blink()
        
    def blink(self):
        self.high()
        time.sleep(2)
        self.low()
        time.sleep(2)
        
    def high(self):
        GPIO.output(self.pin_num,GPIO.HIGH)

    def low(self):
        GPIO.output(self.pin_num,GPIO.LOW)
        
    def clean_up(self):
        GPIO.cleanup()

