import pandas as pd

from config import config
from data_import.data_handler import DataHandler
from util.text_clean_up import clean_up_text
from util.timed_cache import timed_cache


class SongDbDataHandler(DataHandler):
    def __init__(self):
        DataHandler.__init__(self, 'Song DB')
        path = config.input_data_file('billboard_lyrics_1964-2015.csv')
        df = pd.read_csv(path)
        self.df = df[df['Rank'] <= 50]
        self.df = self.df[self.df['Year'] >= 2005]
        self.df = self.df.fillna('')

    def display_labels(self):
        return [[subject, content] for subject, content in
                zip(('Rank '
                     + self.df['Rank'].astype(str)
                     + '. (Year '
                     + self.df['Year'].astype(str)
                     + '): "'
                     + self.df['Song'].str.capitalize()
                     + '" - '
                     + self.df['Artist'].str.capitalize()).tolist(),
                    self.df['Lyrics'].tolist())]

    @timed_cache(minutes=30)
    def __cached_cleanup(self, col):
        return clean_up_text(self.df, col)

    def item_to_cluster(self):
        return [i + ' ' + j for i, j in zip(self.__cached_cleanup('Song'),
                                            self.__cached_cleanup('Lyrics'))]
