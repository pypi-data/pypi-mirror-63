# -*- coding: utf-8 -*-
""" Init Bootstrap """
import json
import yaml

from injector import Injector
import falcon
import importlib
import os.path as path

from routing.controllers.response.custom_response import CustomResponse

class File(object):
    """ File """
    def read(self, file):
        """ read """
        return open(file, 'r+', encoding="utf-8")


class YamlFile(File):
    """ YamlFile """
    def read(self, file):
        """ read """
        file_object = super(YamlFile, self).read(file)
        return yaml.load(file_object)

class FalconApi:

    def __init__(self):
        self.api = falcon.API(
            middleware=[
            ],
            response_type=CustomResponse
        )
        self.__load_routes()

    def __load_routes(self):
        yaml_file = YamlFile()
        file_config = yaml_file.read(path.abspath(path.join(__file__, "../routes.yml")))
        prefix = file_config[0]['prefix']
        routes = file_config[1]['routes']
        injector = Injector()
        for route in routes:
            for resource, handler in route.items():
                module_parts = handler.split('.')
                module_name = '.'.join(module_parts[:-1])
                module = importlib.import_module(module_name)
                handler = getattr(module, module_parts[-1])
                handler_instance = injector.get(handler)
                self.api.add_route(prefix + resource, handler_instance)
