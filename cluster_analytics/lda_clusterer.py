from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from cluster_analytics.cluster_helper import identity_func
from config import config


class LDACluster:
    def __init__(self, documents, n_clusters, top_terms_per_cluster):
        self.documents = documents
        self.top_terms_per_cluster = top_terms_per_cluster
        self.vectorizer = CountVectorizer(max_df=0.8, min_df=2, stop_words=None, tokenizer=identity_func(None),
                                          lowercase=False)
        self.tfidf = self.vectorizer.fit_transform(documents)
        self.features = self.vectorizer.get_feature_names()
        self.clf = LatentDirichletAllocation(n_components=n_clusters,
                                             n_jobs=config.get_env("PROCESSES_NUMBER"),
                                             random_state=0
                                             ).fit(self.tfidf)
        self.topics()

    def get_features_per_topic(self):
        topics = []
        for topic_idx, topic in enumerate(self.clf.components_):
            top_cluster_terms = [self.features[i] for i in topic.argsort()[:-self.top_terms_per_cluster - 1:-1]]
            topics.append([topic_idx, " ".join(top_cluster_terms)])
        return topics

    def topics(self):
        topics = []
        for topic in self.clf.components_:
            topics.append([self.features[i] for i in topic.argsort()[:-self.top_terms_per_cluster - 1:-1]])
        return topics
