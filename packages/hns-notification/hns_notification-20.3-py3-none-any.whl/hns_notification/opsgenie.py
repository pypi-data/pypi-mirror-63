import opsgenie_sdk
import threading

from datetime import datetime


class Opsgenie:

    def __init__(self, key: str, url: str = None):
        """
        Sends alert to opsgenie

        :param key: Opsgenie api key
        :param url: URL/Host of the opsgenie API. By default it is 'https://api.opsgenie.com'. You shouldn't need to
        change it
        """

        self.key = key
        self.url = url

        # Opsgenie api configuration
        conf = opsgenie_sdk.Configuration()
        conf.api_key['Authorization'] = self.key

        if self.url is not None:
            conf.host = self.url

        api_client = opsgenie_sdk.ApiClient(conf)
        self._alert_api = opsgenie_sdk.AlertApi(api_client)

    def _worker(self, alert_body: dict):
        body = opsgenie_sdk.CreateAlertPayload(**alert_body)
        self._alert_api.create_alert(body)

    def _start_thread(self, alert_body: dict):
        t = threading.Thread(target=self._worker, args=(alert_body,))
        t.start()

    def create_alert(self, alert_body: dict):
        """
        Sends the alert to opsgenie
        This always add a `_alert_timestamp` field to the details options in alert body

        :param alert_body: Alert body fields. Check https://docs.opsgenie.com/docs/python-sdk-alert#section-create-alert
        for details on accepted alert body field
        """

        _alert_body = {}
        if alert_body.get('details') is None:
            _alert_body = {**alert_body, **{'details': {'_alert_timestamp': datetime.now()}}}
        else:
            for k, v in alert_body.items():
                if k == 'details':
                    _alert_body[k] = {**v, **{'_alert_timestamp': datetime.now()}}
                else:
                    _alert_body[k] = v
        self._start_thread(_alert_body)
