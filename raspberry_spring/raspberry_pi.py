import RPi.GPIO as GPIO
import time


class RaspberryPiDriver:
    def __init__(self):
        # Use Raspberry Pi board pin number scheme
        GPIO.setmode(GPIO.BOARD)
        
        # Indicate setup to user by blinking GPIO 17
        self.blink(11)
        
    def blink(self, pin):
        self.on(pin)
        time.sleep(2)
        self.off(pin)
        time.sleep(2)
        
    def on(self, pin):
        # Set up GPIO output channel
        GPIO.setup(pin, GPIO.OUT)
        
        GPIO.output(pin ,GPIO.HIGH)

    def off(self, pin):
        # Set up GPIO output channel
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
        
    def clean_up(self):
        print("Cleaning up raspberry pi GPIO")
        GPIO.cleanup()

