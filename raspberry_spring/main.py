import atexit
import time
import urllib

from datadog_client import DatadogClient
from pager_duty_client import PagerDutyClient
from raspberry_pi import RaspberryPi

pi = RaspberryPi()

red_light = 11  # GPIO 17
green_led = 15  # GPIO 15
red_led = 31  # GPIO 6


def exit_handler():
    pi.clean_up()


def main():
    # We should wait for the wifi to connect to a network
    block_until_connected_to_network()

    pager_duty = PagerDutyClient()
    datadog = DatadogClient()
    atexit.register(exit_handler)

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

        # To prevent from using 100% cpu
        time.sleep(0.1)


def block_until_connected_to_network():
    # Letting wifi connect
    light_on = False
    while True:
        try:
            urllib.request.urlopen("http://google.com")
            break
        except urllib.error.URLError as e:
            print("Couldn't connect to Network" + e.reason)
            pi.on(red_light)
            light_on = True
        time.sleep(5)
    if light_on:
        pi.off(red_light)


if __name__ == '__main__':
    main()
