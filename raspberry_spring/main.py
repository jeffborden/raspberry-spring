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

    # TODO remove this or something later.. this is just to show us it's working
    print(client.get_outstanding_pager_duty_alerts_for_service(verbose=True, service_id='PNN\
RR6Q'))
    print(client.get_outstanding_pager_duty_alerts_for_service(verbose=True))

    red_light_pin = 11 # GPIO 17

    while True:
        if client.light_should_be_on():
            pi.on(red_light_pin)
        else:
            pi.off(red_light_pin)
        time.sleep(10)


