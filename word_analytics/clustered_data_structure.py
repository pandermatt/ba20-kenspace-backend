class ClusteredStructure:
    __slots__ = ['text', 'cluster']

    def __init__(self, text, cluster):
        self.text = text
        self.cluster = cluster
