from config import config
from word_analytics.clustered_data_structure import ClusteredStructure
from word_analytics.document_reader import DocumentReader
from word_analytics.k_means_clusterer import KCluster


def generate_cluster():
    path = config.data_file('imdb-f.csv')
    doc_reader = DocumentReader(path)
    data_list = doc_reader.rows  # titles, contents, story-plots

    k_cluster = KCluster(get_all_titles(data_list), 10, 10000)

    return prepare_clustered_data_structure(get_all_titles(data_list), k_cluster)


def get_all_titles(data_list):
    titles = []
    for i in range(len(data_list[:])):
        titles.append(data_list[:][i][0])
    return titles


def prepare_clustered_data_structure(text_list, k_cluster):
    structured_data = []
    for i in range(len(text_list)):
        text = text_list[i]
        prediction = k_cluster.make_prediction(text)
        structured_data.append(ClusteredStructure(text, cluster_data_as_text(prediction, k_cluster.terms)))
    return structured_data


def cluster_data_as_text(cluster, terms):
    data = []
    for i in range(len(cluster)):
        data.append(terms[cluster[i]])
    return data
