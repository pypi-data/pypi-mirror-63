from unittest import TestCase
from unittest.mock import patch, Mock
from routing.infrastructure.proxy.openrouteservice.distancematrix_client import DistanceMatrixClient

class TestDistanceMatrixClient(TestCase):
    _response_openrouteservice = {
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

    _client_input = {'units': 'km', 'metrics': ['duration', 'distance'], 'locations': [[-77.0792794, -12.0716139], [-77.0769189, -12.0716924]]}
    """
    @patch('routing.infrastructure.proxy.openrouteservice.distancematrix_client.requests.post')
    @patch('bootstrap.config.config_yaml.ConfigYaml')
    def test_getMatrix(self, requests_post, ConfigYaml):
        config = ConfigYaml
        mockresponse = Mock()
        mockresponse.json.return_value = self._response_openrouteservice
        config.get_key.return_value = {"distancematrix": "test_url"}
        requests_post.return_value = mockresponse
        client = DistanceMatrixClient(config)
        client.token = "token"
        response = client.getMatrix(self._client_input)
        self.assertEqual(client.get_headers(), {'Authorization': "token"})
        self.assertEqual(response.status_code, 200)

    @patch('routing.infrastructure.proxy.openrouteservice.distancematrix_client.requests.post')
    @patch('bootstrap.config.config_yaml.ConfigYaml')
    def should_rise_exception(self, requests_post, ConfigYaml):
        config = ConfigYaml
        config.get_key.return_value = {"distancematrix": "test_url"}
        requests_post.return_value = Exception('Test')
        client = DistanceMatrixClient(config)
        self.assertRaises(Exception, client.getMatrix, self._client_input)
"""
