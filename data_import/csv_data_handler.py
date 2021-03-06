import os

import pandas as pd

from api.errors import error_response
from config import config
from data_import.data_handler import DataHandler, calculate_n_clusters_by_category


class CsvDataHandler(DataHandler):
    def __init__(self, name, csv_file, default_sep=","):
        DataHandler.__init__(self, name)
        path = config.input_data_file(csv_file)
        df = pd.read_csv(path, default_sep)
        self.df = df.fillna('')


class MovieDbHandler(CsvDataHandler):
    """
    Dataset Source:
    https://www.kaggle.com/rounakbanik/the-movies-dataset#movies_metadata.csv
    """

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
    http://insideairbnb.com/get-the-data.html
    """

    def __init__(self, settings):
        data_source = settings['city']
        if data_source not in ['amsterdam', 'athens', 'barcelona', 'berlin', 'bologna',
                               'dublin', 'geneva', 'hongkong', 'westernaustralia']:
            error_response(f'{data_source} does not exist')

        CsvDataHandler.__init__(self, f'AirBnBDB{data_source}', f'{data_source}_listings_details.csv')

        self.HAS_MULTIPLE_DATA_SOURCES = True
        self.DATA_SOURCE = data_source
        self.PRE_LOAD_UUID = f'AirBnB-Demo-{data_source}'

        self.df = self.df[:4_000]
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
        release_dates = self.df['price'].tolist()
        ratings = self.df['review_scores_rating'].tolist()
        urls = self.df['listing_url'].tolist()

        return [{
            "content": content,
            "image": image,
            "rating": self.round_int(rating),
            "release_date": release_date,
            "data_url": url
        } for content, image, rating, release_date, url in zip(contents, images, ratings, release_dates, urls)]

    def calculate_n_clusters(self):
        return calculate_n_clusters_by_category(self.df.shape[0])['small'][1]

    @staticmethod
    def round_int(value):
        try:
            return round(int(value) / 20)
        except ValueError:
            return 0


class CustomCSV(CsvDataHandler):
    def __init__(self, settings):
        CsvDataHandler.__init__(self, 'Custom', os.path.join('custom', f"{settings['filename']}.csv"))
        self.SHUFFLE_DATA = False

        self.settings = settings
        self.cluster_size = settings['clusterSize']
        # self.df = self.df[:1_000]

        if settings['itemToAnalyse'] == 'all':
            self.saved_item_to_cluster = [i + j for i, j in
                                          zip(self.clean_up_text_from_settings('display', settings),
                                              self.clean_up_text_from_settings('content', settings))]
        else:
            self.saved_item_to_cluster = self.clean_up_text_from_settings('content', settings)

    def clean_up_text_from_settings(self, df_col, settings):
        return self.clean_up_df_text(settings[df_col],
                              language=settings['language'],
                              clean_up_method=settings['techniques'],
                              second_language=settings['secondLanguage'])

    def display_labels(self):
        return self.df[self.settings['display']].tolist()

    def meta_info(self):
        return [{"content": content} for content in self.df[self.settings['content']].tolist()]

    def calculate_n_clusters(self):
        return calculate_n_clusters_by_category(self.df.shape[0])[self.cluster_size][1]
