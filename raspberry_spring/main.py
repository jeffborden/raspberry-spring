import time

from raspberry_light import RaspberryLight
from pager_duty_client import PagerDutyClient

import atexit


def exit_handler():
    print('My application is ending!')
    pi.clean_up()
    print('cleaned up pi')


atexit.register(exit_handler)
pi = RaspberryLight(11)
client = PagerDutyClient()
    
# TODO remove this or something later.. this is just to show us it's working
print(client.get_outstanding_pager_duty_alerts_for_service(verbose=True, service_id='PNN\
RR6Q'))

print(client.get_outstanding_pager_duty_alerts_for_service(verbose=True))



while True:
    if client.light_should_be_on():
        pi.high()
    else:
        pi.low()
    time.sleep(10)


