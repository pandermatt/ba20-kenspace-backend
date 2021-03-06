from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from cluster_analytics.cluster_helper import identity_func
from config import config


class KMeansCluster:
    def __init__(self, documents, n_clusters, top_terms_per_cluster, max_iteration):
        self.documents = documents
        self.n_clusters = n_clusters
        self.top_terms_per_cluster = top_terms_per_cluster
        self.max_iteration = max_iteration

        self.vectorizer = None
        self.tfidf_matrix = None
        self.model = None

        self.calculate()

    def calculate(self, stopwords=None):
        self.vectorizer = TfidfVectorizer(stop_words=stopwords, max_df=0.8, tokenizer=identity_func(stopwords),
                                          lowercase=False)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

        self.model = KMeans(n_clusters=self.n_clusters,
                            init='k-means++',
                            max_iter=self.max_iteration,
                            n_init=1,
                            n_jobs=config.get_env("PROCESSES_NUMBER"))
        self.model.fit(self.tfidf_matrix)

    def make_prediction_as_text(self, text_to_predict):
        y = self.vectorizer.transform([text_to_predict])
        index = self.model.predict(y)

        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names()

        prediction_list = order_centroids[int(index), :self.top_terms_per_cluster]
        return [terms[prediction] for prediction in prediction_list]

    def print_clusters(self):
        print("Top terms per cluster:")
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names()
        for i in range(self.model.n_clusters):
            print("Cluster %d:" % i),
            for ind in order_centroids[i, :self.top_terms_per_cluster]:
                print(' %s' % terms[ind])
            print()

    def get_terms(self):
        terms = self.vectorizer.get_feature_names()

        terms_list = []

        for idx, doc in enumerate(self.documents):
            feature_index = self.tfidf_matrix[idx, :].nonzero()[1]
            tfidf_scores = zip(feature_index, [self.tfidf_matrix[idx, x] for x in feature_index])
            sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
            doc_terms = [w for w, s in [(terms[i], s) for (i, s) in sorted_scores[:self.top_terms_per_cluster]]]
            terms_list.append(doc_terms)

        return terms_list

    def get_clusters(self):
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names()
        clusters = []
        for i in range(self.model.n_clusters):
            entry = []
            for ind in order_centroids[i, :self.top_terms_per_cluster]:
                entry.append(terms[ind])
            clusters.append(entry)
        return clusters

    def get_cluster_id(self):
        return self.model.labels_
