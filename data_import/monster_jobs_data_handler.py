import pandas as pd

from config import config
from data_import.data_handler import DataHandler
from util.text_clean_up import clean_up_text
from util.timed_cache import timed_cache


class MonsterDataHandler(DataHandler):
    def __init__(self):
        DataHandler.__init__(self, 'Monster')
        path = config.input_data_file('monster-jobs2.csv')
        df = pd.read_csv(path)
        self.df = df.fillna('')

    def display_labels(self):
        return self.df['job-title'].tolist()

    @timed_cache(minutes=30)
    def __cached_cleanup(self, col):
        return clean_up_text(self.df, col)

    def item_to_cluster(self):
        return [i + ' ' + j for i, j in zip(self.__cached_cleanup('job-subtitle'),
                                            self.__cached_cleanup('job-content'))]
