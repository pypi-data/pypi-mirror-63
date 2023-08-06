# -*- coding: utf-8 -*-
"""Initialize Phalcon Framework"""

from bootstrap import FalconApi


class App:
    """Class App Base"""

    def __init__(self):
        self.api = FalconApi().api
