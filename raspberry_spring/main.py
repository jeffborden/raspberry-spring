import time

from raspberry_pi import RaspberryPi
from pager_duty_client import PagerDutyClient

import atexit



def exit_handler():
    pi.clean_up()


if __name__ == '__main__':
    pi = RaspberryPi()
    client = PagerDutyClient()
    atexit.register(exit_handler)

    red_light = 11      # GPIO 17
    green_led = 15      # GPIO 15
    red_led = 31        # GPIO 6
    
    while True:
        if client.light_should_be_on():
            pi.on(red_light)
        else:
            pi.off(red_light)
        time.sleep(10)


