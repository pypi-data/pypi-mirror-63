# -*- coding: utf-8 -*-
import requests
from dataclasses import dataclass
from injector import inject, singleton
from requests.exceptions import HTTPError
from bootstrap.config.config_yaml import ConfigYaml

@inject
@singleton
@dataclass
class DistanceMatrixClient:
    _config: ConfigYaml

    __uri = None
    __headers = None

    def getMatrix(self, uri_params, query, headers = None):
        uri = self.get_url()
        try:
            response = requests.get(uri + uri_params, query)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        return response.json()

    @property
    def token(self):
        pass

    @token.setter
    def token(self, token):
        self.__headers = {'Authorization': token}

    def get_headers(self):
        return self.__headers

    def get_url(self):
        if self.__uri == None:
            self.__uri = self._config.get_key('openrouteservice')
        return self.__uri['distancematrix']

    def close(self):
        del self
