"""Module Client pour ZentuxLog"""
import urllib.parse

import json
import requests
import threading


from zentuxlog_client.endpoint import EndPoint
from zentuxlog_client.errors import (
    RequestError,
    ResponseCodeError,
    TimeoutCustomError,
    AuthMissing
)


class Client:
    """
    Un client permet de requêter l'api déployée.
    """

    def __init__(self, auth, settings, async_call=False):
        """Constructeur."""
        self.id_client = auth['client_id']
        self.auth = auth
        settings.__dict__.update(self.auth)
        self.settings = settings
        self.payload = None
        self.endpoint = EndPoint(settings=self.settings)
        self.async_call = async_call
        self.token = None

    def send(self, data=None, logfile=None, method="GET", path=None, protected=True, headers=None, daemon=True):
        """
        @param data: Data to be sent to API
        """
        data_call = {
            "method": method,
            "path": path,
            "protected": protected,
            "headers": headers
        }
        if not data and logfile:
            for log in logfile.generate(daemon):
                data_call.update({"data": log})
                if self.async_call:
                    t = threading.Thread(target=self.__call_api, kwargs=data_call)
                    t.start()
                else:
                    self.__call_api(**data_call)
        else:
            data_call.update({'data': data})
            if self.async_call:
                t = threading.Thread(target=self.__call_api, kwargs=data_call)
                return t.start()
            else:
                return self.__call_api(**data_call)

    def __call_api(self, **kwargs):
        timeout = self.settings.timeout
        uri = self.endpoint.get_uri()
        headers = kwargs['headers']
        protected = kwargs['protected']
        data = {
            "data": kwargs['data'],
            "sensor": self.settings.sensor_name
        }
        path = kwargs['path']
        method = kwargs['method']

        if not headers:
            headers = dict()

        if protected:
            if not self.token:
                self.__fetch_token()

            if data and self.token:
                bearer = "Bearer {token}".format(token=self.token)
                headers.update({
                    'Authorization': bearer
                })

        if path:
            uri = urllib.parse.urljoin(uri, path)
        try:
            if method == 'PUT':
                raise NotImplementedError
            elif method == 'GET':
                return self.__get(uri, timeout, headers)
            elif method == 'POST':
                return self.__post(json.dumps(data), uri, timeout, headers)
            elif method == 'DELETE':
                raise NotImplementedError
        except requests.exceptions.Timeout:
            raise TimeoutCustomError("Timeout atteint: {} ms".format(timeout))
        except requests.exceptions.RequestException as e:
            raise RequestError(e)

    def check(self):
        """
        Vérification de l'api
        """
        return self.send()

    def __fetch_token(self):
        """Méthode privée qui permet de récupérer le token."""
        data = {
                'grant_type': 'password',
                'username': self.settings.username,
                'password': self.settings.password,
                }

        response = self.__post(
            data=data,
            uri=self.endpoint.get_url_token(),
            auth=(self.settings.client_id, self.settings.client_secret),
            timeout=self.settings.timeout
            )
        if 'access_token' in response:
            self.token = response['access_token']
        else:
            raise AuthMissing

    def _get_http_headers(self, additional_headers=None):
        headers = {}
        headers = self.settings.headers
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def __get(self, uri, timeout, custom_headers):
        response = requests.get(uri,
                                headers=self._get_http_headers(custom_headers),
                                timeout=timeout)
        self.__check_errors(response)
        return response.json()

    def __post(self, data, uri, timeout, headers=None, auth=None):
        if headers:
            headers = self._get_http_headers(headers)
        response = requests.post(uri, data=data, headers=headers, timeout=timeout, auth=auth)
        self.__check_errors(response)
        return response.json()

    @staticmethod
    def __check_errors(response):
        status_code = response.status_code
        if status_code == 200 or status_code == 201:
            return
        raise ResponseCodeError(status_code, response.text)
