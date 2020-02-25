from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer


class AgglomerativeTextCluster:
    def __init__(self, data):
        self.data = data
        self.clusterCount = int(len(data) / 6)  # cluster size
        print("cluster count: {0}, data size: {1}".format(self.clusterCount, len(self.data)))
        self.vectorizer = TfidfVectorizer()
        self.model = AgglomerativeClustering(n_clusters=self.clusterCount)
        self.vectorizer.fit_transform(self.data)

    def __make_prediction(self, text_to_predict):
        self.__predict(text_to_predict)
        index = self.__last_index()
        return self.__get_cluster(index)

    def __predict(self, text_to_predict):
        d = self.data.copy()
        d.append(text_to_predict)
        y = self.vectorizer.transform(d)
        self.model.fit_predict(y.toarray())

    def __last_index(self):
        last = len(self.data)
        return self.model.labels_[last]  # get cluster number

    def __get_cluster(self, index):
        cluster = []
        for i in range(0, len(self.data)):
            if self.model.labels_[i] == index:
                cluster.append(self.data[i])
        return cluster

    def get_prediction_cluster(self, text_to_predict):
        return self.__make_prediction(text_to_predict)
