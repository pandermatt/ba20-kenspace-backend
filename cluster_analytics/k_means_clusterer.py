import uuid

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from config import config


class KMeansCluster:
    def __init__(self, documents, top_terms_per_cluster, max_iteration):
        self.uuid = str(uuid.uuid4())
        self.documents = documents
        self.top_terms_per_cluster = top_terms_per_cluster
        self.max_iteration = max_iteration

        self.vectorizer = None
        self.tfidf_matrix = None
        self.model = None

        self.calculate()

    def calculate(self, stopwords=None):
        self.vectorizer = TfidfVectorizer(stop_words=stopwords, max_df=0.8)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

        self.model = KMeans(
            n_clusters=int(len(self.documents) / 5),
            init="k-means++",
            max_iter=self.max_iteration,
            n_init=1,
            n_jobs=config.get_env("PROCESSES_NUMBER"),
        )
        self.model.fit(self.tfidf_matrix)

    def make_prediction_as_text(self, text_to_predict):
        y = self.vectorizer.transform([text_to_predict])
        index = self.model.predict(y)

        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names()

        prediction_list = order_centroids[int(index), :self.
                                          top_terms_per_cluster]
        return [terms[prediction] for prediction in prediction_list]

    def print_clusters(self):
        print("Top terms per cluster:")
        order_centroids = self.model.cluster_centers_.argsort()[:, ::-1]
        terms = self.vectorizer.get_feature_names()
        for i in range(self.model.n_clusters):
            print("Cluster %d:" % i),
            for ind in order_centroids[i, :self.top_terms_per_cluster]:
                print(" %s" % terms[ind])
            print()

    def get_terms_as_text(self):
        terms = self.vectorizer.get_feature_names()

        terms_list = []

        for idx, doc in enumerate(self.documents):
            feature_index = self.tfidf_matrix[idx, :].nonzero()[1]
            tfidf_scores = zip(
                feature_index,
                [self.tfidf_matrix[idx, x] for x in feature_index])
            sorted_scores = sorted(tfidf_scores,
                                   key=lambda x: x[1],
                                   reverse=True)
            doc_terms = [
                w for w, s in [(terms[i], s) for (
                    i, s) in sorted_scores[:self.top_terms_per_cluster]]
            ]
            terms_list.append(doc_terms)

        # Todo: Print Cluster ID (j) to a new array
        return [x + [str(j)] for x, j in zip(terms_list, self.model.labels_)]
