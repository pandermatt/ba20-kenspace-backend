from os.path import exists, join

from api import errors
from config import config
from data_import import imdb_data_handler, email_data_handler, whats_app_data_handler, recipe_data_handler, \
    monster_jobs_data_handler, song_db_data_handler
from data_import.data_handler import DataHandler
from file_io import storage_io
from util.logger import log
from util.timed_cache import timed_cache


@timed_cache(minutes=100)
def initialize_data(selected_data: str) -> DataHandler:
    """
    Specifies which DataHandler to use
    """

    data_handler = {'Imdb': imdb_data_handler.ImdbDataHandler,
                    'Email': email_data_handler.EmailDataHandler,
                    'WhatsApp': whats_app_data_handler.WhatsAppDataHandler,
                    'Recipe': recipe_data_handler.RecipeDataHandler,
                    'Monster': monster_jobs_data_handler.MonsterDataHandler,
                    'SongDb': song_db_data_handler.SongDbDataHandler}

    if exists(config.model_data_file(f'data-{selected_data}.sav')):
        return storage_io.load_data_from_disk(selected_data)

    if selected_data not in data_handler.keys():
        log.warn(f'{selected_data} not found')
        return errors.unauthorized_response()

    data_handler_factory = data_handler[selected_data]()
    storage_io.save_data_to_disk(data_handler_factory, selected_data)

    return data_handler_factory
