from config import config
from util.logger import log
from util.text_clean_up import clean_up_text


class DataHandler:
    TOP_TERMS_PER_CLUSTER = config.get_env("DEFAULT_TOP_TERMS_PER_CLUSTER")
    SHUFFLE_DATA = True

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

    def clean_up_df_text(self, col, language="english"):
        return clean_up_text(self.df, col, language)

    def calculate_n_clusters(self):
        """
        map function: maps document size to n_clusters
        """
        document_size = self.df.shape[0]
        upper_limit = config.get_env("N_CLUSTERS_UPPER_LIMIT")
        result = ((17 * document_size) + 29800) / 9990
        if result >= upper_limit:
            result = upper_limit
        return round(document_size / result)
