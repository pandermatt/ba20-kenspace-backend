import pandas as pd

from config import config
from util.logger import log
from util.noun_extraction import extract_nouns
from word_analytics.clustered_data_structure import ClusteredStructure
from word_analytics.k_means_clusterer import KCluster


def generate_cluster():
    log.info("Generating Clusters")
    path = config.data_file('imdb-f.csv')
    df = pd.read_csv(path)
    df = df.fillna('')

    all_titles = get_column(df, 'movie-title')

    result = [i + ' ' + j for i, j in zip(extract_nouns(df, 'movie-content'),
                                          extract_nouns(df, 'story-line'))]

    k_cluster = KCluster(result, 10, 10000)
    return prepare_clustered_data_structure(all_titles, k_cluster)


def get_column(df, col_name):
    return df[col_name].tolist()


def prepare_clustered_data_structure(text_list, k_cluster):
    structured_data = []
    for text in text_list:
        prediction = k_cluster.make_prediction(text)
        structured_data.append(ClusteredStructure(text, cluster_data_as_text(prediction, k_cluster.terms)))
    return structured_data


def cluster_data_as_text(cluster_list, terms):
    data = []
    for cluster in cluster_list:
        data.append(terms[cluster])
    return data
