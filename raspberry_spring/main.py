import argparse
import atexit
import time

from pager_duty_client import PagerDutyClient
from datadog_client import DatadogClient
from output import OutputService

pi = None


def exit_handler():
    pi.clean_up()

def main():

    global pi  # pylint: disable=global-statement

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', help='If flag is '
                        'present, does not run geocode lookup.')
    params = parser.parse_args()

    if not params.test:
        time.sleep(5)

    pi = OutputService(params.test)

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
        pi.on(green_led)
        for t in times:
            state = not state
            if state:
                pi.on(green_led)
            else:
                pi.off(green_led)
            time.sleep(t)
        pi.off(green_led)

        time.sleep(0.1)

if __name__ == '__main__':
    main()
