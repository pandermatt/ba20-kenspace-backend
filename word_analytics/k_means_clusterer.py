from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer


class KCluster:
    def __init__(self, data, data_per_cluster, max_iteration):
        self.data_per_cluster = data_per_cluster
        self.max_iteration = max_iteration
        self.model = None
        self.fitted_values = None
        self.centroids_ordered = None
        self.data = data
        self.terms = None
        self.vectorizer = TfidfVectorizer()
        self.cluster_count = int(len(data) / data_per_cluster) * 100

        self.__set_k_mean_model(self.cluster_count,
                                self.__vectorize_data())
        self.__set_centroids()
        self.__set_terms()

    def __set_k_mean_model(self, true_k, x):
        self.model = cluster.KMeans(n_clusters=true_k, init='k-means++', max_iter=self.max_iteration, n_init=1)
        self.fitted_values = self.model.fit(x)

    def __vectorize_data(self):
        return self.vectorizer.fit_transform(self.data)

    def __set_centroids(self):
        self.centroids_ordered = self.model.cluster_centers_.argsort()[:, ::-1]

    def __set_terms(self):
        self.terms = self.vectorizer.get_feature_names()

    def __get_prediction_cluster(self, index):
        return self.centroids_ordered[int(index), :self.data_per_cluster]

    def make_prediction(self, text_to_predict):
        index = self.prediction_index(text_to_predict)
        return self.__get_prediction_cluster(index)

    def prediction_index(self, textToPredict):
        y = self.vectorizer.transform([textToPredict])
        return self.model.predict(y)

    def fitted_values(self, data):
        vector_data = self.vectorizer.transform(data)
        return self.model.fit(vector_data)
