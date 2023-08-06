from unittest import TestCase
from unittest.mock import patch
from routing.infrastructure.proxy.openrouteservice.distancematrix_adapter import DistanceMatrixAdapter

class TestDistanceMatrixAdapter(TestCase):

    def setUp(self):
        pass

    @patch('routing.infrastructure.proxy.openrouteservice.distancematrix_client.DistanceMatrixClient')
    def test_getMatrix(self, ClientMock):
        client = ClientMock
        matrix_request = [
            {
                "latitude": -12.0716139,
                "longitude": -77.0792794,
                "type": "hub",
                "serviceTime": 0,
                "orderPointId": "hub"
            },
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
        client.getMatrix.return_value = {
            "metadata": {
                "attribution": "openrouteservice.org, OpenStreetMap contributors",
                "service": "matrix",
                "timestamp": 1581975876529,
                "query": {
                    "locations": [
                        [
                            -77.0792794,
                            -12.0716139
                        ],
                        [
                            -77.0769189,
                            -12.0716924
                        ]
                    ],
                    "profile": "driving-car",
                    "responseType": "json",
                    "metrics": [
                        "distance",
                        "duration"
                    ],
                    "units": "km"
                },
                "engine": {
                    "version": "5.0.2",
                    "build_date": "2020-01-30T19:19:31Z"
                }
            },
            "durations": [
                [
                    0.0,
                    146.39
                ],
                [
                    158.62,
                    0.0
                ]
            ],
            "distances": [
                [
                    0.0,
                    0.93
                ],
                [
                    0.93,
                    0.0
                ]
            ],
            "destinations": [
                {
                    "location": [
                        -77.078873,
                        -12.071705
                    ],
                    "snapped_distance": 45.28
                },
                {
                    "location": [
                        -77.076919,
                        -12.071688
                    ],
                    "snapped_distance": 0.44
                }
            ],
            "sources": [
                {
                    "location": [
                        -77.078873,
                        -12.071705
                    ],
                    "snapped_distance": 45.28
                },
                {
                    "location": [
                        -77.076919,
                        -12.071688
                    ],
                    "snapped_distance": 0.44
                }
            ]
        }

        distancematrix_adapter = DistanceMatrixAdapter(client)
        distancematrix_result = distancematrix_adapter.getMatrix(matrix_request)
        latitude_location_0 = distancematrix_result['metadata']['query']['locations'][0][1]
        self.assertEqual(latitude_location_0, -12.0716139)
