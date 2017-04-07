import time
import os
from random import randint
from typing import List
from unittest.mock import MagicMock

from datadog import initialize, api

def mock_response(*args, **kwargs):
    del args, kwargs
    point_list = []
    timestamp = float(time.time()) * 1000.0
    last_time = timestamp - 600000

    for _ in range(0, randint(0, 10)):
        num_orders = float(randint(0, 2))
        point_list.append([last_time, num_orders])
        last_time += randint(1, 6)

    return {'status': 'ok', 'to_date': timestamp, 'series': [{'pointlist': point_list}]}

class DatadogClient:
    def __init__(self, test: bool=False) -> None:
        # Seconds to pretend that we're in the past
        self.latency = 125
        self.query_frequency = 120

        api_key = os.environ.get('DATADOG_API_KEY', None)
        app_key = os.environ.get('DATADOG_APP_KEY', None)

        options = {
            'api_key': api_key,
            'app_key': app_key
        }

        initialize(**options)
        self.query = 'sum:spring.counter.multi_item_cart.order_placed{run_mode:4real}.as_count()'
        # self.query = 'sum:aws.elb.request_count{name:sfe-4real-elb}.as_count()'

        self.last_query_time = time.time() - self.latency
        self.orders = []  # type: List

        if test:
            # pylint: disable=redefined-outer-name
            api.Metric.query = MagicMock(side_effect=mock_response)


    def get_orders(self) -> bool:
        now = time.time()
        result = api.Metric.query(start=int(self.last_query_time), end=int(now), query=self.query)

        if result['status'] != 'ok':
            return False

        self.last_query_time = result['to_date'] / 1000
        if len(result['series']) > 0:
            self.orders += list(filter(lambda p: p[1] != 0.0, result['series'][0]['pointlist']))
        return True


    def get_light_times(self) -> List[float]:

        delayed_now = time.time() - self.latency
        times = []  # type: List[float]
        while len(self.orders) > 0:
            order = self.orders[0]
            if order[0] / 1000 <= delayed_now:
                print("Orders: " + str(order[1]) + " (" + str(order[0]) + ")")
                for _ in range(0, int(order[1])):
                    times += [1.0, 0.5]
                self.orders.pop(0)
            else:
                break
        return times

    def run(self) -> None:
        if self.last_query_time + self.query_frequency < float(time.time()):
            self.get_orders()


if __name__ == "__main__":
    client = DatadogClient()
    while True:
        client.run()
        time.sleep(0.1)
