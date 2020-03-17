import pandas as pd

from config import config
from data_import.data_handler import DataHandler


class CsvDataHandler(DataHandler):
    def __init__(self, name, csv_file):
        DataHandler.__init__(self, name)
        path = config.input_data_file(csv_file)
        df = pd.read_csv(path)
        self.df = df.fillna('')


class MonsterDataHandler(CsvDataHandler):
    def __init__(self):
        CsvDataHandler.__init__(self, 'Monster', 'monster-jobs2.csv')
        self.TOP_TERMS_PER_CLUSTER = 100
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('job-subtitle'),
                                                            self.clean_up_df_text('job-content'))]

    def display_labels(self):
        return self.df['job-title'].tolist()


class RecipeDataHandler(CsvDataHandler):
    def __init__(self):
        CsvDataHandler.__init__(self, 'Recipe', 'epicurious.csv')
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('reciepe-title'),
                                                            self.clean_up_df_text('reciepe-content'))]

    def display_labels(self):
        return self.df['reciepe-title'].tolist()


class ImdbDataHandler(CsvDataHandler):
    def __init__(self):
        CsvDataHandler.__init__(self, 'IMDB', 'imdb-f.csv')
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('movie-content'),
                                                            self.clean_up_df_text('story-line'))]

    def display_labels(self):
        return [[subject, content] for subject, content in
                zip(self.df['movie-title'].tolist(), self.df['story-line'].tolist())]


class MovieDbHandler(CsvDataHandler):
    def __init__(self):
        CsvDataHandler.__init__(self, 'MovieDB', 'movies_metadata.csv')
        self.df = self.df[:1000]
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('overview'),
                                                            self.clean_up_df_text('original_title'))]

    def display_labels(self):
        return [[subject, content] for subject, content in
                zip(self.df['original_title'].tolist(), self.df['overview'].tolist())]
