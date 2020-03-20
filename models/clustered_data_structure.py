import json


class RestDisplayStructure:
    __slots__ = ['text', 'content', 'terms', 'cluster_id', 'meta_info']

    def __init__(self, text, meta_info, terms, cluster_id):
        self.text = text
        self.meta_info = meta_info
        self.terms = terms
        self.cluster_id = str(cluster_id)
