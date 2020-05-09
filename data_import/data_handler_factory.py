import json
from os.path import exists

from api import errors
from config import config
from data_import import email_data_handler, song_db_data_handler, csv_data_handler
from data_import.data_handler import DataHandler
from file_io import storage_io
from util.logger import log
from util.timed_cache import timed_cache


@timed_cache(minutes=100)
def initialize_data(selected_data: str, settings) -> DataHandler:
    """
    Specifies which DataHandler to use
    """

    if settings:
        settings = json.loads(settings)

        if selected_data == 'custom':
            return initialize_custom_data(csv_data_handler.CustomCSV,
                                          settings,
                                          settings['identifier'])

        if selected_data == 'AirBnBDb':
            return initialize_custom_data(csv_data_handler.AirBnBHandler,
                                          settings,
                                          f"{selected_data}-{settings['city']}")

    return initialize_normal_data(selected_data)


def initialize_normal_data(selected_data):
    data_handler = {
        'Email': email_data_handler.EmailDataHandler,
        'MovieDb': csv_data_handler.MovieDbHandler,
        'SongDb': song_db_data_handler.SongDbDataHandler
    }

    if exists(config.model_data_file(f'data-{selected_data}.sav')):
        return storage_io.load_data_from_disk(selected_data)

    if selected_data not in data_handler.keys():
        log.warn(f'{selected_data} not found')
        errors.unauthorized_response()

    data_handler_factory = data_handler[selected_data]()
    storage_io.save_data_to_disk(data_handler_factory, selected_data)

    return data_handler_factory


def initialize_custom_data(handler, settings, identifier):
    if exists(config.model_data_file(f"data-{identifier}.sav")):
        return storage_io.load_data_from_disk(identifier)

    custom_data = handler(settings)
    storage_io.save_data_to_disk(custom_data, identifier)

    return custom_data
