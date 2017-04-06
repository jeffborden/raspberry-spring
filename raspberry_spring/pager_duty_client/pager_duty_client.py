import os
import requests
import logging


def getPagerDutyAlerts():
    logging.basicConfig(level=logging.DEBUG)

    authToken = os.environ.get('PAGERDUTY_API_KEY', None)
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": "Token token="+authToken,
    }
    # response = requests.get('https://api.pagerduty.com/services', headers=headers)
    response = requests.get('https://api.pagerduty.com/alerts', headers=headers)
    if response:
        try:
            print(response.text)
            json_response = response.json()
            return json_response
        except:
            print("Couldn't parse response: "+response)
    else:
        print("DIDN'T GET A RESPONSE")
    return None

response = getPagerDutyAlerts()
# if response is not None and response.get('services') is not None:
#     d = {}
#     for service in response.get('services'):
#         d[service.get('name')] = service.get('id')
#     print(d)


if response is not None and response.get('alerts') is not None:
    d = {}
    for alert in response.get('alerts'):
        d[alert.get('id')] = alert.get('status')
        # service = alert.get('service')
        # if service is not None and service.get('summary') is not None:
        #     d[service.get('summary')] = alert
    print(d)

