# -*- coding: utf-8 -*-
import falcon

class CustomResponse(falcon.Response):

    def __init__(self, options=None):
        super().__init__(options)
        self._code = None
        self._msg = None
        self._data = None
        self.status = falcon.HTTP_200

    @property
    def code(self):
        return self._msg

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def message(self):
        return self._msg

    @message.setter
    def message(self, message):
        self._msg = message

    @property
    def data_response(self):
        return self._data

    @data_response.setter
    def data_response(self, data):
        self._data = data
        self.media = {
            'code': self._code if self._code else 1000,
            'message': self._msg,
            'data': data
        }
