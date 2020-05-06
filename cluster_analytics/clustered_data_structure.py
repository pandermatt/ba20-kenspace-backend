from cluster_analytics.k_means_clusterer import KMeansCluster
from cluster_analytics.lda_clusterer import LDACluster


class ClusterIO:
    def __init__(self, uuid: str, k_means: KMeansCluster, lda: LDACluster, topics):
        self.uuid = uuid
        self.k_means = k_means
        self.lda = lda
        self.topics = topics


class RestDisplayStructure:
    __slots__ = ['text', 'content', 'terms', 'cluster_id', 'meta_info']

    def __init__(self, text, meta_info, terms, cluster_id):
        self.text = text
        self.meta_info = meta_info
        self.terms = terms
        self.cluster_id = str(cluster_id)


class RestDisplayStructureKenSemble:
    __slots__ = ['cluster_id', 'terms']

    def __init__(self, terms, cluster_id):
        """
        link lda topic terms to k_means cluster_id
        """
        self.terms = terms
        self.cluster_id = str(cluster_id)
