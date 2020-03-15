import pandas as pd

from config import config
from data_import.data_handler import DataHandler


class ImdbDataHandler(DataHandler):
    def __init__(self):
        DataHandler.__init__(self, 'IMDB')
        path = config.input_data_file('imdb-f.csv')
        df = pd.read_csv(path)
        self.df = df.fillna('')
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('movie-content'),
                                                            self.clean_up_df_text('story-line'))]

    def display_labels(self):
        return [[subject, content] for subject, content in
                zip(self.df['movie-title'].tolist(), self.df['story-line'].tolist())]
