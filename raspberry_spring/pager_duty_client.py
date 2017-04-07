
import logging
import os

import requests
        
class PagerDutyClient:
    def __init__(self) -> None:
        auth_token = os.environ.get('PAGERDUTY_API_KEY', None)
        self.common_headers = {
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Authorization": "Token token=" + auth_token,
        }

    def light_should_be_on(self):
        # TODO fill this in
        return True
        
    def get_pager_duty_alerts(self, **kwargs):
        if 'verbose' in kwargs:
            logging.basicConfig(level=logging.DEBUG)

        if 'endpoint_url' in kwargs:
            endpoint_url = kwargs['endpoint_url']
        else:
            endpoint_url = 'https://api.pagerduty.com/alerts'

        response = requests.get(endpoint_url, headers=self.common_headers)
        if response:
            try:
                json_response = response.json()
                # print(response.text)
                return json_response
            except:
                if 'verbose' in kwargs:
                    print("Couldn't parse response: " + response)
        else:
            if 'verbose' in kwargs:
                print("DIDN'T GET A RESPONSE")
        return None

    # This function will get all outstanding pagerduty alerts and return
    # a mapping from alert status to a count of the number of alerts with that status
    #
    # arguments:
    #     service_id: if set, the return value will only consider alerts for the specified service
    #     service_name: if set, the return value will only consider alerts for the specified service
    def get_outstanding_pager_duty_alerts_for_service(self, **kwargs):
        all_alerts = self.get_pager_duty_alerts(**kwargs)
        if all_alerts is not None and all_alerts.get('alerts') is not None:
            hist = {}
            for alert in all_alerts.get('alerts'):
                if 'service_id' in kwargs:
                    service = alert.get('service')
                    if service is None or service.get('id') != kwargs.get(
                            'service_id'):
                        continue

                if 'service_name' in kwargs:
                    service = alert.get('service')
                    if service is None or service.get('summary') != kwargs.get(
                            'service_name'):
                        continue

                status = alert.get('status')
                if status is None:
                    continue
                elif status in hist:
                    hist[status] = hist[status] + 1
                else:
                    hist[status] = 1
        return hist
