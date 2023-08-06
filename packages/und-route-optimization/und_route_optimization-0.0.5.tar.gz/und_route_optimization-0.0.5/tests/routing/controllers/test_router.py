import json
import falcon
from urllib.parse import urlencode
from falcon import testing
from unittest import TestCase
from unittest.mock import patch
from routing.controllers.router import RouterController
from routing.controllers.response.custom_response import CustomResponse

class TestRouterController(TestCase):

    def setUp(self):
        super(TestRouterController, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = falcon.API(
            middleware=[
            ]
        )

    @patch('routing.services.router_service.RouterService')
    def test_on_post(self, RouterServiceMock):
        router_service = RouterServiceMock()
        response =  [
            {
                "stops": [
                    {
                        "latitude": -12.0716139,
                        "longitude": -77.0792794,
                        "arrive": "7:00",
                        "orderId": "hub"
                    },
                    {
                        "latitude": -12.0716924,
                        "longitude": -77.0769189,
                        "arrive": "07:02",
                        "orderId": "os-1"
                    },
                    {
                        "latitude": -12.0716139,
                        "longitude": -77.0792794,
                        "arrive": "07:10",
                        "orderId": "hub"
                    }
                ],
                "duration": "00 horas 10: minutos 05 segundos",
                "distance": "1.86 km",
                "vehicleId": "a"
            }
        ]
        router_service.createRoutes.return_value = response
        router_controller = RouterController(router_service)
        router_request = {
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
        self.app.add_route("/routing", router_controller)
        result = falcon.testing.simulate_post(app=self.app, path="/routing", json=router_request)
        self.assertEqual(result.status, falcon.HTTP_200)
