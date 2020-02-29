import pandas as pd

from config import config
from data_import.data_handler import DataHandler
from util.text_clean_up import clean_up_text


class ImdbDataHandler(DataHandler):
    def __init__(self):
        DataHandler.__init__(self, 'IMDB')
        path = config.input_data_file('imdb-f.csv')
        df = pd.read_csv(path)
        self.df = df.fillna('')
        pass

    def display_labels(self):
        return self.df['movie-title'].tolist()

    def item_to_cluster(self):
        return [i + ' ' + j for i, j in zip(clean_up_text(self.df, 'movie-content'),
                                            clean_up_text(self.df, 'story-line'))]
