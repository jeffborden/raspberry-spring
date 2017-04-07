import logging
import os
from copy import copy
from typing import List

import requests


class PagerDutyClient:
    def __init__(self) -> None:
        auth_token = os.environ.get('PAGERDUTY_API_KEY', None)
        self.common_headers = {
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Authorization": "Token token=" + auth_token,
        }

    def get_pager_duty_alerts(self, **kwargs):
        """
        This function will pull a JSON encoded response from the Pagerduty incidents endpoint
          
        :param kwargs: 
            # verbose: boolean, Indicates if we should print debugging info
            # endpoint_url: string, The url of the incidents endpoint for PagerDuty
            # statuses: string[], A list of status codes to filter on (e.g. ['triggered', 'acknowledged'])
            # service_ids: string[], A list of service_ids to filter on (e.g. ['PNNRR6Q']
        :return: 
            a JSON encoded object or None
        """
        if 'verbose' in kwargs and kwargs['verbose']:
            logging.basicConfig(level=logging.DEBUG)

        if 'endpoint_url' in kwargs:
            endpoint_url = kwargs['endpoint_url']
        else:
            endpoint_url = 'https://api.pagerduty.com/incidents'

        request_data = {}
        if 'statuses' in kwargs:
            request_data['statuses[]'] = kwargs['statuses']
        if 'service_ids' in kwargs:
            request_data['service_ids[]'] = kwargs['service_ids']

        response = requests.get(
            endpoint_url, headers=self.common_headers, data=request_data)
        if response:
            try:
                json_response = response.json()
                return json_response
            except:
                if 'verbose' in kwargs and kwargs['verbose']:
                    print("Couldn't parse response: " + response)
        else:
            if 'verbose' in kwargs and kwargs['verbose']:
                print("DIDN'T GET A RESPONSE")
        return None

    def has_triggered_alerts_for_service(self,
                                         service_ids: List[str],
                                         **kwargs):
        pagerduty_response = self.get_pager_duty_alerts(
            service_ids=service_ids, statuses=['triggered'], **kwargs)
        if pagerduty_response is not None and pagerduty_response.get(
                'incidents') is not None:
            return len(pagerduty_response.get('incidents')) > 0
        return False

    def light_should_be_on(self):
        # TODO fill this in
        return True


# client = PagerDutyClient()
# client.has_triggered_alerts_for_service(service_ids=['PNNRR6Q'], verbose=True)

# {
#     'Catalog-Eng': 'PUZRE98',
#     'cloudwatch': 'PSP00LK',
#     'Datadog - Elasticsearch - Low': 'P3T3EJY',
#     'Datadog - High Urgency': 'P5QQOOM',
#     'Datadog - ETL Engineer Sev 2': 'P9KVWRC',
#     'DataDog App Support Engineer Sev 2': 'P4FD9EE',
#     'Datadog - Email Scraper Engineer Sev 3': 'PFII32W',
#     'Datadog - Low Urgency': 'PNNRR6Q',
#     'Datadog - BMV3 Engineer Sev 2': 'PDB1NGR',
#     'Datadog - App Support Engineer Sev 1': 'PZDS807',
#     'Merchandising': 'PINBL01',
#     'Pingdom': 'PROVYJV',
#     'Calypso-Fire': 'PRM0123',
#     'Datadog - ETL Engineer Sev 1': 'P0K47QZ',
#     'graylog': 'PZRWW4Q',
#     'Team urgency': 'P73W5N8',
#     'Datadog - Elasticsearch - High': 'PZ851UT',
#     'Datadog - Bmv3 Engineer Sev 1': 'P804Y3X'
# }
