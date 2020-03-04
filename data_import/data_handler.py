from util.logger import log


class DataHandler:
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
        map function: map document size to n_clusters
        """
        document_size = self.df.shape[0]
        upper_limit = 20
        result = ((17 * document_size) + 29800)/9990
        if result >= upper_limit:
            result = 20
        return round(document_size/result)

