import argparse
import atexit
import time
import requests


from pager_duty_client import PagerDutyClient
# from datadog_client import DatadogClient
from output import OutputService

pi = None

red_light = 11  # GPIO 17
green_led = 15  # GPIO 15
red_led = 31  # GPIO 6


def exit_handler():
    pi.clean_up()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', help='disabled raspi stuff')
    parser.add_argument('-d', '--ddtest', action='store_true', help='mocks datadog data')
    params = parser.parse_args()

    if not params.test:
        time.sleep(5)

    global pi  # pylint: disable=global-statement
    pi = OutputService(params.test)

    # We should wait for the wifi to connect to a network
    block_until_connected_to_network()

    pager_duty = PagerDutyClient()
    # datadog = DatadogClient(params.ddtest)
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

        # datadog.run()
        # times = datadog.get_light_times()
        # state = True
        # for t in times:
        #     if state:
        #         pi.on(green_led)
        #     else:
        #         pi.off(green_led)
        #     state = not state
        #     time.sleep(t)

        # To prevent from using 100% cpu
        time.sleep(0.1)


def block_until_connected_to_network():
    # Letting wifi connect
    light_on = False
    while True:
        try:
            requests.get("http://shopspring.com", timeout=5)
            break
        except requests.exceptions.Timeout as e:
            # TODO something with e.reason
            print("Couldn't connect to Network")
            pi.on(red_light)
            light_on = True
        time.sleep(5)
    if light_on:
        pi.off(red_light)


if __name__ == '__main__':
    main()
