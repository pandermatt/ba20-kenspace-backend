from config import config
from data_import import imdb_data_handler, email_data_handler, whats_app_data_handler, recipe_data_handler, \
    monster_jobs_data_handler, song_db_data_handler
from data_import.data_handler import DataHandler
from util.timed_cache import timed_cache


@timed_cache(minutes=100)
def initialize_data() -> DataHandler:
    """
    Specifies which DataHandler to use
    """

    data_handler = {'Imdb': imdb_data_handler.ImdbDataHandler,
                    'Email': email_data_handler.EmailDataHandler,
                    'WhatsApp': whats_app_data_handler.WhatsAppDataHandler,
                    'Recipe': recipe_data_handler.RecipeDataHandler,
                    'Monster': monster_jobs_data_handler.MonsterDataHandler,
                    'SongDb': song_db_data_handler.SongDbDataHandler}
    return data_handler[config.get_env("DATA")]()
