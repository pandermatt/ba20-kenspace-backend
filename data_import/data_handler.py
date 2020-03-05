from util.logger import log
from config import config


class DataHandler:
    TOP_TERMS_PER_CLUSTER = config.get_env("DEFAULT_TOP_TERMS_PER_CLUSTER")

    def __init__(self, name):
        self.name = name
        log.info(f'{name} Data Loaded')
        self.df = None

    def display_labels(self):
        pass

    def item_to_cluster(self):
        pass

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
