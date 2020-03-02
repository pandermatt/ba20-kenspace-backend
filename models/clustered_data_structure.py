class ClusteredStructure:
    __slots__ = ['text', 'content', 'cluster']

    def __init__(self, text, cluster):
        if isinstance(text, list):
            self.text = text[0]
            self.content = text[1]
        else:
            self.text = text
            self.content = ""
        self.cluster = cluster
