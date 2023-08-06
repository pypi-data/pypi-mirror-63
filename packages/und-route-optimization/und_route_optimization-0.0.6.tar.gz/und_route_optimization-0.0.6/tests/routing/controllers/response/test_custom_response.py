import falcon
from unittest import TestCase
from routing.controllers.response.custom_response import CustomResponse

class TestCustomRequest(TestCase):

    def test_constructor(self):
        custom_response = CustomResponse()
        custom_response.code = "response_message"
        custom_response.message = "response_message"
        custom_response.data_response = {"data": "response"}

        self.assertEqual(custom_response.code, "response_message")
        self.assertEqual(custom_response.message, "response_message")
