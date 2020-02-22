import os
from os.path import dirname, abspath, join

import yaml

from util.logger import log


class Config:
    _root_dir = dirname(abspath(__file__))
    _application_config_path = join(_root_dir, 'application.yml')
    _config_file = None

    def auth_key(self):
        return self._get_var('AUTH_KEY')

    def _get_var(self, var):
        if not self._config_file:
            try:
                with open(self._application_config_path, 'r') as stream:
                    self._config_file = yaml.safe_load(stream)
                    log.info("Config Loaded")
            except FileNotFoundError:
                log.info("Config not found, using ENV Var")
                return os.environ.get(var)
        try:
            return os.environ.get(var) or self._config_file[var]
        except KeyError:
            log.error('Can not find ENV var: %s' % var)


config = Config()
