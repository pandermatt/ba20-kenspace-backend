import os

import pandas as pd

from config import config
from data_import.data_handler import DataHandler, calculate_n_clusters_by_category


class CsvDataHandler(DataHandler):
    def __init__(self, name, csv_file, default_sep=","):
        DataHandler.__init__(self, name)
        path = config.input_data_file(csv_file)
        df = pd.read_csv(path, default_sep)
        self.df = df.fillna('')


class MovieDbHandler(CsvDataHandler):
    def __init__(self):
        CsvDataHandler.__init__(self, 'MovieDB', 'movies_metadata.csv')
        self.df = self.df[:10_000]
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('overview'),
                                                            self.clean_up_df_text('original_title'))]

    def display_labels(self):
        return self.df['original_title'].tolist()

    def meta_info(self):
        return [{"content": content, "image": 'https://image.tmdb.org/t/p/w185' + image} for content, image in
                zip(self.df['overview'].tolist(), self.df['poster_path'].tolist())]


class CustomCSV(CsvDataHandler):
    def __init__(self, settings):
        CsvDataHandler.__init__(self, 'Custom', os.path.join('custom', settings['filename']))
        self.SHUFFLE_DATA = False

        self.settings = settings
        self.cluster_size = settings['clusterSize']
        self.saved_item_to_cluster = [i + j for i, j in
                                      zip(self.clean_up_df_text(settings['display'],
                                                                language=settings['language'],
                                                                clean_up_method=settings['techniques']),
                                          self.clean_up_df_text(settings['content'],
                                                                language=settings['language'],
                                                                clean_up_method=settings['techniques']))]

    def display_labels(self):
        return self.df[self.settings['display']].tolist()

    def meta_info(self):
        return [{"content": content} for content in self.df[self.settings['content']].tolist()]

    def calculate_n_clusters(self):
        return calculate_n_clusters_by_category(self.df.shape[0])[self.cluster_size][1]
