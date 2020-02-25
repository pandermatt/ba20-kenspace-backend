from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer

from config import config


class KCluster:
    def __init__(self, data, data_per_cluster, max_iteration):
        self.data_per_cluster = data_per_cluster
        self.max_iteration = max_iteration
        self.model = None
        self.fitted_values = None
        self.centroids_ordered = None
        self.features = None
        self.vectorizer = TfidfVectorizer(max_df=0.8)
        self.cluster_count = int(len(data) / data_per_cluster * 10)

        self.__set_k_mean_model(self.cluster_count,
                                self.vectorizer.fit_transform(data))

        self.centroids_ordered = self.model.cluster_centers_.argsort()[:, ::-1]
        self.features = self.vectorizer.get_feature_names()

    def __set_k_mean_model(self, n_clusters, data):
        self.model = cluster.KMeans(n_clusters=n_clusters, init='k-means++', max_iter=self.max_iteration, n_init=1)
        self.fitted_values = self.model.fit(data)

    def __get_prediction_cluster(self, index):
        return self.centroids_ordered[int(index), :self.data_per_cluster]

    def make_prediction(self, text_to_predict):
        index = self.prediction_index(text_to_predict)
        return self.__get_prediction_cluster(index)

    def prediction_index(self, text_to_predict):
        y = self.vectorizer.transform([text_to_predict])
        return self.model.predict(y)

    def fitted_values(self, data):
        vector_data = self.vectorizer.transform(data)
        return self.model.fit(vector_data)
