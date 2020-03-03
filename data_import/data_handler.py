from util.logger import log


class DataHandler:
    def __init__(self, name):
        self.name = name
        log.info(f'{name} Data Loaded')

    def display_labels(self):
        pass

    def item_to_cluster(self):
        pass
