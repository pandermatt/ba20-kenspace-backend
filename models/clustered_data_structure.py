class ClusteredStructure:
    __slots__ = ['text', 'content', 'terms', 'cluster_id']

    def __init__(self, text, terms, cluster_id):
        if isinstance(text, list):
            self.text = text[0]
            self.content = text[1]
        else:
            self.text = text
            self.content = ""
        self.terms = terms
        self.cluster_id = cluster_id
