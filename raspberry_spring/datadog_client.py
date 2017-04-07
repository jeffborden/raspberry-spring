import time
import os
from typing import List

from datadog import initialize, api

class DatadogClient:
    def __init__(self) -> None:
        # Seconds to pretend that we're in the past
        self.latency = 65
        self.query_frequency = 60

        api_key = os.environ.get('DATADOG_API_KEY', None)
        app_key = os.environ.get('DATADOG_APP_KEY', None)

        options = {
            'api_key': api_key,
            'app_key': app_key
        }

        initialize(**options)
        self.query = 'sum:spring.counter.multi_item_cart.order_placed{run_mode:4real}.as_count()'

        self.last_query_time = time.time() - self.latency
        self.orders = []


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
        times = []
        while len(self.orders) > 0:
            order = self.orders[0]
            if order[0] / 1000 <= delayed_now:
                print("Orders: " + str(order[1]) + " (" + str(order[0]) + ")")
                for i in range(0, int(order[1])):
                    times += [1000, 500]
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
