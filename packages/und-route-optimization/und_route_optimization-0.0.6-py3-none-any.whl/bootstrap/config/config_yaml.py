from .base import BaseConfig
from bootstrap import YamlFile
import sys
import collections
import glob
import os


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


class ConfigYaml(BaseConfig):
    configs = {}
    yaml_file = YamlFile()
    path_config = "config/config.yml"
    try:
        path_config = os.environ["CONFIG_PATH"]
    except KeyError:
        print("La variable de configuracion CONFIG_PATH no fue declarada")

    configs = yaml_file.read(path_config)

    def __init__(self):
        self._config = self.configs
