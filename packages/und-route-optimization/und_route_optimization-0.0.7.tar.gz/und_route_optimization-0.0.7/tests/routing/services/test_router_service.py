from unittest import TestCase
from unittest.mock import patch
from routing.services.router_service import RouterService

class TestRouterReservive(TestCase):
    _create_routes_spected = [
        {
            "stops": [
                {
                    "latitude": -12.0716139,
                    "longitude": -77.0792794,
                    "arrive": "7:00",
                    "orderId": "hub",
                    "deltaTime": 0,
                    "deltaStartTime": 0,
                    "deltaDistance": 0
                },
                {
                    "latitude": -12.0716924,
                    "longitude": -77.0769189,
                    "arriveLabel": "07:02",
                    "orderId": "os-1",
                    "deltaTime": 154,
                    "deltaStartTime": 154,
                    "deltaDistance": 929
                },
                {
                    "latitude": -12.0716139,
                    "longitude": -77.0792794,
                    "arriveLabel": "07:10",
                    "orderId": "hub",
                    "deltaTime": 179,
                    "deltaStartTime": 633,
                    "deltaDistance": 926
                }
            ],
            "durationLabel": "00 horas 10 minutos 32 segundos",
            "distanceLabel": "1856 m",
            "duration": 633,
            "distance": 1856,
            "vehicleId": "a"
        }
    ]
    _router_sservice_input = {
        "start": "7:00",
        "origin": {
            "latitude": -12.0716139,
            "longitude": -77.0792794,
            "type": "hub",
            "serviceTime": 0,
            "orderPointId": "hub"
        },
        "vehicles": [
            {
                "vehicleId": "a",
                "volumeCapacity": 40,
                "weightCapacity": 40,
                "maxDistance": 200
            }
        ],
        "orders": [
            {
                "longitude": -77.0769189,
                "latitude": -12.0716924,
                "type": "os",
                "volume": 2,
                "weight": 2,
                "orderPointId": "os-1",
                "serviceTime": 300
            }
        ]
    }
    _distancematrix_result = {
        'code': 'Ok',
        'distances': [[0, 929.4], [926.4, 0]],
        'durations': [[0, 154.1], [178.7, 0]],
        'sources': [
            {
                'hint': 'S8ACgNy_AoBRAAAAaAAAAEEBAAAAAAAARTwHQocdLEKTPwVDAAAAAFEAAABoAAAAQQEAAAAAAACJAAAAp95n--fMR_8R3Wf7Qs1H_wIADwyDOYs6',
                'distance': 45.334433,
                'location': [-77.078873, -12.071705],
                'name': ''
            },
            {
                'hint': 'mw4ZgP___3-uAAAALgEAAAAAAABTAAAAwUjpQm-tqUIAAAAAPiheQq4AAAAuAQAAAAAAAFMAAACJAAAASeZn-_jMR_9J5mf79MxH_wAA_xCDOYs6',
                'distance': 0.442466,
                'location': [-77.076919, -12.071688],
                'name': 'Paracas'
                }
            ],
        'destinations': [
            {
                'hint': 'S8ACgNy_AoBRAAAAaAAAAEEBAAAAAAAARTwHQocdLEKTPwVDAAAAAFEAAABoAAAAQQEAAAAAAACJAAAAp95n--fMR_8R3Wf7Qs1H_wIADwyDOYs6',
                'distance': 45.334433,
                'location': [-77.078873, -12.071705],
                'name': ''
            },
            {
                'hint': 'mw4ZgP___3-uAAAALgEAAAAAAABTAAAAwUjpQm-tqUIAAAAAPiheQq4AAAAuAQAAAAAAAFMAAACJAAAASeZn-_jMR_9J5mf79MxH_wAA_xCDOYs6',
                'distance': 0.442466,
                'location': [-77.076919, -12.071688],
                'name': 'Paracas'
            }
        ]
    }

    _vrp_solver_result = [[0, 1, 0]]

    @patch('routing.infrastructure.proxy.openrouteservice.distancematrix_adapter.DistanceMatrixAdapter')
    @patch('routing.optimization.vrp_solver.VRPSolver')
    def test_create_routes(self, DistanceMatrixMock, VrpSolverMock):
        distancematrix_adapter = DistanceMatrixMock
        vrp_solver = VrpSolverMock
        distancematrix_adapter.getMatrix.return_value = self._distancematrix_result
        vrp_solver.solve.return_value = self._vrp_solver_result
        routerService = RouterService(vrp_solver, distancematrix_adapter)
        result = routerService.createRoutes(self._router_sservice_input)
        self.assertEqual(self._create_routes_spected, result)
