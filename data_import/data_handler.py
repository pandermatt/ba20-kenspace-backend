from config import config
from util.logger import log
from util.text_clean_up import clean_up_text


class DataHandler:
    TOP_TERMS_PER_CLUSTER = config.get_env("DEFAULT_TOP_TERMS_PER_CLUSTER")
    SHUFFLE_DATA = True
    PRE_LOAD_UUID = None

    def __init__(self, name):
        self.name = name
        log.info(f'{name} Data Loaded')
        self.df = None
        self.saved_item_to_cluster = None

    def display_labels(self):
        pass

    def meta_info(self):
        return [{"content": ''}] * self.df.shape[0]

    def item_to_cluster(self):
        return self.saved_item_to_cluster

    def clean_up_df_text(self, col, language="english", clean_up_method="nltk"):
        return clean_up_text(self.df, col, language, clean_up_method)

    def calculate_n_clusters(self):
        return calculate_n_clusters_by_category(self.df.shape[0])['medium'][1]


def calculate_n_clusters_by_category(document_size):
    """
    map function: maps document size to n_clusters
    """
    result_large = (29702 * document_size + 14914915) / 5000000
    result_medium = (17 * document_size + 29800) / 9990
    result_small = (4702 * document_size + 32812813) / 11000000

    return {
        'large': [round(result_large), round(document_size / result_large)],
        'medium': [round(result_medium), round(document_size / result_medium)],
        'small': [round(result_small), round(document_size / result_small)],
    }
