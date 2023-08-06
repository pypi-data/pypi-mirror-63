import time
from urllib import parse as urlparse

import requests
import jwt


class Client(object):
    api_base_url = 'https://datahub.moyiquant.com/api/'

    def __init__(self, user, password):
        self._user = user
        self._password = password
        self._access_token = None

    def fetch(self, url, timeout=30):
        if self._is_access_token_expired():
            self._update_access_token()

        return self._fetch(url, timeout)

    def _fetch(self, url, timeout):
        url = urlparse.urljoin(Client.api_base_url, url)
        headers = {'Authorization': 'Bearer {token}'.format(
            token=self._access_token)}
        req = requests.get(url, headers=headers, timeout=timeout)
        req.raise_for_status()
        return req.json()

    def _update_access_token(self):
        url = urlparse.urljoin(Client.api_base_url, 'token')
        data = {'email': self._user, 'password': self._password}

        req = requests.post(url, json=data, timeout=30)
        req.raise_for_status()
        self._access_token = req.json()['access']

    def _is_access_token_expired(self):
        if not self._access_token:
            return True

        payload = self._decode(self._access_token)
        if payload['exp'] - 30 <= time.time():
            return True
        return False

    def _decode(self, token):
        return jwt.decode(token, verify=False)
