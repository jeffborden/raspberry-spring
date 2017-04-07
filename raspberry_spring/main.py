import time

from raspberry_pi import RaspberryPi
from pager_duty_client import PagerDutyClient
from datadog_client import DatadogClient

import atexit



def exit_handler():
    pi.clean_up()


if __name__ == '__main__':
    pi = RaspberryPi()
    pager_duty = PagerDutyClient()
    datadog = DatadogClient()
    atexit.register(exit_handler)

    red_light = 11      # GPIO 17
    green_led = 15      # GPIO 15
    red_led = 31        # GPIO 6

    last_pager_duty_update = int(time.time())
    pager_duty_update_frequency = 60

    while True:
        now = int(time.time())
        if last_pager_duty_update + pager_duty_update_frequency < now:
            if pager_duty.light_should_be_on():
                pi.on(red_light)
            else:
                pi.off(red_light)
            last_pager_duty_update = now

        datadog.run()
        times = datadog.get_light_times()
        state = True
        GPIO.output(green_led, GPIO.HIGH)
        for t in times:
            state = not state
            if state:
                GPIO.output(green_led, GPIO.HIGH)
            else:
                GPIO.output(green_led, GPIO.LOW)
            time.sleep(t)
        GPIO.output(green_led, GPIO.LOW)

        time.sleep(0.1)

