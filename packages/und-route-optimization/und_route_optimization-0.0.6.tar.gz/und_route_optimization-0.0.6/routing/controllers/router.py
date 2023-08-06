# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from injector import inject
from routing.controllers.response.custom_response import CustomResponse
from routing.services.router_service import RouterService

@inject
@dataclass
class RouterController:
    _router_service: RouterService

    def on_post(self, req, resp: CustomResponse):
        resp.message = 'Peticion Exitosa.'
        try:
            data_set = json.loads(req.bounded_stream.read())
        except Exception as err:
            print(err)
            data_set = []
        response = self._router_service.createRoutes(data_set)
        resp.data_response = response
