# hns_notification
Thin wrapper around various notification systems. 

## Notifications available
1. Opsgenie

## Installation
`pip install hns-notification`

## Opsgenie usage
Below code snippet shows how to create alert on opsgenie. 
```python
# Import Opsgenie Class
from hns_notification.opsgenie import Opsgenie
# Your API key
api_key = 'api_key'

# Instantiate Opsgenie class
ops_genie = Opsgenie(api_key)

# Create the alert, pass the alert message body. 
# This always add a `_alert_timestamp` field to the details options in alert body
# Check https://docs.opsgenie.com/docs/python-sdk-alert#section-create-alert for details on accepted alert body fields.  
ops_genie.create_alert({
    'message': 'sample_msg',
    'alias': 'some-alias',
    'responders': [{
                'name': 'SampleTeam',
                'type': 'team'
              }],
    'visible_to': [
      {'name': 'Sample',
       'type': 'team'}],
    'actions': ['Restart', 'AnExampleAction'],
    'tags': ['OverwriteQuietHours'],
    'details': {'key1': 'value1',
             'key2': 'value2'},
    'entity': 'An example entity',
    'priority': 'P3',
    'description': 'Sample of SDK v2'
})
```
