from dataclasses import dataclass
from injector import inject
from datetime import timedelta, datetime, time
from time import strftime, gmtime
from routing.infrastructure.proxy.openrouteservice.distancematrix_adapter import DistanceMatrixAdapter
from routing.optimization.vrp_solver import VRPSolver

@inject
@dataclass
class RouterService:
    _vrp_solver: VRPSolver
    _distancematrix_adapter: DistanceMatrixAdapter

    def createRoutes(self, route_input):
        delivery_points = route_input['stops']
        delivery_points.insert(0,route_input['origin'])
        distancematrix_response = self._distancematrix_adapter.getMatrix(delivery_points)
        optimize_result = self._vrp_solver.solve(
            distancematrix_response['durations'],
            1,
            0)
        routes_result = list()
        for route_index, route in enumerate(optimize_result):
            route_data = {}
            route_data["stops"] = list()
            total_duration = 0
            total_distance = 0
            for i, item in enumerate(route[1:len(route)-1], start=1):
                current_index = route[i]
                previous_index = route[i-1]
                distance = distancematrix_response['distances'][previous_index][current_index]
                duration = distancematrix_response['durations'][previous_index][current_index]
                arrive_time = duration
                total_duration += arrive_time
                total_distance += distance
                delta_arrive = timedelta(seconds=+arrive_time)
                route_data["stops"].append({
                    'stopIndex': current_index-1,
                    'deltaTime': round(duration),
                    'deltaDistance': round(distance)
                })
            route_data['duration'] = round(total_duration)
            route_data['distance'] = round(total_distance)
            routes_result.append(route_data)
        return routes_result
