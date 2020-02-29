import uuid

from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer


class KMeansCluster:
    def __init__(self, data, data_per_cluster, max_iteration):
        self.uuid = str(uuid.uuid4())
        self.data = data
        self.data_per_cluster = data_per_cluster
        self.max_iteration = max_iteration

        self.vectorizer = None
        self.model = None
        self.centroids_ordered = None
        self.features = None

        self.calculate()

    def calculate(self, stopwords=None):
        self.vectorizer = TfidfVectorizer(max_df=0.8, stop_words=stopwords, max_features=10000)

        cluster_count = int(len(self.data) / self.data_per_cluster * 3)
        data = self.vectorizer.fit_transform(self.data)
        self.model = cluster.KMeans(n_clusters=cluster_count, init='k-means++', max_iter=self.max_iteration, n_init=1)
        self.model.fit(data)

        self.centroids_ordered = self.model.cluster_centers_.argsort()[:, ::-1]
        self.features = self.vectorizer.get_feature_names()

    def __make_prediction(self, text_to_predict):
        index = self.__prediction_index(text_to_predict)
        return self.__get_prediction_cluster(index)

    def __prediction_index(self, text_to_predict):
        y = self.vectorizer.transform([text_to_predict])
        return self.model.predict(y)

    def __get_prediction_cluster(self, index):
        return self.centroids_ordered[int(index), :self.data_per_cluster]

    def make_prediction_as_text(self, text_to_predict):
        prediction_list = self.__make_prediction(text_to_predict)
        return [self.features[prediction] for prediction in prediction_list]
