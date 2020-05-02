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
        self.PRE_LOAD_UUID = "MovieDB-Demo"
        self.df = self.df[:10_000]
        self.saved_item_to_cluster = [i + j for i, j in zip(self.clean_up_df_text('overview'),
                                                            self.clean_up_df_text('original_title'))]

    def display_labels(self):
        return self.df['original_title'].tolist()

    def meta_info(self):
        contents = self.df['overview'].tolist()
        images = self.df['poster_path'].tolist()
        ratings = self.df['vote_average'].tolist()
        release_dates = self.df['release_date'].tolist()
        image_prefix = 'https://image.tmdb.org/t/p/w185'

        return [{
            "content": content,
            "image": f'{image_prefix}{image}',
            "rating": round(rating / 2),
            "release_date": release_date.split("-")[0]
        } for content, image, rating, release_date in zip(contents, images, ratings, release_dates)]


class AirBnBHandler(CsvDataHandler):
    """
    Dataset Source:
    https://www.kaggle.com/brittabettendorf/berlin-airbnb-data#listings_summary.csv
    """

    def __init__(self):
        CsvDataHandler.__init__(self, 'AirBnBDB', 'listings_summary.csv')
        self.PRE_LOAD_UUID = "AirBnB-Demo"
        self.df = self.df[:1_000]
        self.saved_item_to_cluster = [i + j + k + l for i, j, k, l in zip(self.clean_up_df_text('description'),
                                                                          self.clean_up_df_text('space'),
                                                                          self.clean_up_df_text(
                                                                              'neighborhood_overview'),
                                                                          self.clean_up_df_text('transit'))]

    def display_labels(self):
        return self.df['name'].tolist()

    def meta_info(self):
        contents = self.df['summary'].tolist()
        images = self.df['picture_url'].tolist()
        release_dates = self.df['listing_url'].tolist()

        return [{
            "content": content,
            "image": image,
            "release_date": release_date
        } for content, image, release_date in zip(contents, images, release_dates)]


class CustomCSV(CsvDataHandler):
    def __init__(self, settings):
        CsvDataHandler.__init__(self, 'Custom', os.path.join('custom', f"{settings['filename']}.csv"))
        self.SHUFFLE_DATA = False

        self.settings = settings
        self.cluster_size = settings['clusterSize']

        if settings['itemToAnalyse'] == 'all':
            self.saved_item_to_cluster = [i + j for i, j in
                                          zip(self.clean_up_df_text(settings['display'],
                                                                    language=settings['language'],
                                                                    clean_up_method=settings['techniques']),
                                              self.clean_up_df_text(settings['content'],
                                                                    language=settings['language'],
                                                                    clean_up_method=settings['techniques']))]
        else:
            self.saved_item_to_cluster = self.clean_up_df_text(settings['content'],
                                                               language=settings['language'],
                                                               clean_up_method=settings['techniques'])

    def display_labels(self):
        return self.df[self.settings['display']].tolist()

    def meta_info(self):
        return [{"content": content} for content in self.df[self.settings['content']].tolist()]

    def calculate_n_clusters(self):
        return calculate_n_clusters_by_category(self.df.shape[0])[self.cluster_size][1]
