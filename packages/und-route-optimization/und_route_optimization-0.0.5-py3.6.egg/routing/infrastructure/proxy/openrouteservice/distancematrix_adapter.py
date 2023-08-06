import json
from dataclasses import dataclass
from datetime import timedelta, datetime, time
from time import strftime, gmtime
from injector import inject, singleton
from routing.infrastructure.proxy.openrouteservice.distancematrix_client import DistanceMatrixClient

@inject
@singleton
@dataclass
class DistanceMatrixAdapter:
    _client: DistanceMatrixClient

    def getMatrix(self, points):
        query_params = dict()
        query_params['annotations'] = 'duration,distance'
        locations = []
        request_string="http://localhost:5000/table/v1/driving/"
        for point in points:
            locations.append(str(point['longitude']) + ',' + str(point['latitude']))
        uir_params = ";".join(locations)
        start_process_time = datetime.now();
        response = self._client.getMatrix(uir_params, query_params)
        finish_process_time = datetime.now();
        delta = finish_process_time - start_process_time
        return self._client.getMatrix(uir_params, query_params)
