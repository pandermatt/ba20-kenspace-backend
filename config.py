import os
from os.path import dirname, abspath, join, exists

import yaml

from util.logger import log
from util.timed_cache import timed_cache


def get_or_create(dir_path):
    if not exists(dir_path):
        os.makedirs(dir_path)
        log.info("Creating: " + dir_path)
    return dir_path


@timed_cache(minutes=100)
def initialize_data():
    """
    Specifies which DataHandler to use
    """
    from data_import.imdb_data_handler import ImdbDataHandler
    from data_import.email_data_handler import EmailDataHandler
    from data_import.whats_app_data_handler import WhatsAppDataHandler
    from data_import.recipe_data_handler import RecipeDataHandler
    from data_import.monster_jobs_data_handler import MonsterDataHandler
    from data_import.yt_videos_data_handler import YouTubeVideosDataHandler

    data_handler = {'Imdb': ImdbDataHandler,
                    'Email': EmailDataHandler,
                    'WhatsApp': WhatsAppDataHandler,
                    'Recipe': RecipeDataHandler,
                    'Monster': MonsterDataHandler,
                    'YTVideos': YouTubeVideosDataHandler}
    return data_handler[config.get_env("DATA")]()


class Config:
    __root_dir = dirname(abspath(__file__))
    __application_config_path = join(__root_dir, 'application.yml')
    __config_file = None

    def __data_dir(self):
        return get_or_create(abspath(join(self.__root_dir, 'data')))

    def input_data_dir(self):
        return get_or_create(join(self.__data_dir(), 'input'))

    def input_data_file(self, file_name):
        return join(self.input_data_dir(), file_name)

    def model_data_dir(self):
        return get_or_create(join(self.__data_dir(), 'model'))

    def model_data_file(self, file_name):
        return join(self.model_data_dir(), file_name)

    def get_env(self, var):
        return self.__get_var(var)

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
