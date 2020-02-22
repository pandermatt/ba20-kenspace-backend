import os
from os.path import dirname, abspath, join, exists

import yaml

from util.logger import log


def get_or_create(dir_path):
    if not exists(dir_path):
        os.makedirs(dir_path)
        log.info("Creating: " + dir_path)
    return dir_path


class Config:
    __root_dir = dirname(abspath(__file__))
    __application_config_path = join(__root_dir, 'application.yml')
    __config_file = None

    def __data_dir(self):
        return get_or_create(abspath(join(self.__root_dir, 'data')))

    def data_file(self, file_name):
        return join(self.__data_dir(), file_name)

    def auth_key(self):
        return self.__get_var('AUTH_KEY')

    def __get_var(self, var):
        if not self.__config_file:
            try:
                with open(self.__application_config_path, 'r') as stream:
                    self.__config_file = yaml.safe_load(stream)
                    log.info("Config Loaded")
            except FileNotFoundError:
                log.info("Config not found, using ENV Var")
                return os.environ.get(var)
        try:
            return os.environ.get(var) or self.__config_file[var]
        except KeyError:
            log.error('Can not find ENV var: %s' % var)


config = Config()
