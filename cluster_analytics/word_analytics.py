import threading

import nltk
import pandas as pd

from cluster_analytics.agglomerative_clusterer import AgglomerativeTextCluster
from cluster_analytics.k_means_clusterer import KCluster
from config import config
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.text_clean_up import clean_up_text


def generate_cluster():
    log.info('Generating Clusters: ID {0}'.format(threading.current_thread().ident))
    path = config.data_file('imdb-f.csv')
    df = pd.read_csv(path)
    df = df.fillna('')

    all_titles = get_column(df, 'movie-title')

    log.info('Starting Text Cleanup ID {0}'.format(threading.current_thread().ident))
    result = [i + ' ' + j for i, j in zip(clean_up_text(df, 'movie-content'),
                                          clean_up_text(df, 'story-line'))]

    log.info('Starting prediction: ID {0}'.format(threading.current_thread().ident))
    k_cluster = KCluster(result, 10, 10000)
    return prepare_clustered_data_structure(all_titles, k_cluster)


def get_column(df, col_name):
    return df[col_name].tolist()


def prepare_clustered_data_structure(text_list, k_cluster):
    structured_data = []
    for text in text_list:
        prediction = k_cluster.make_prediction(text)
        structured_data.append(ClusteredStructure(text, cluster_data_as_text(prediction, k_cluster.features)))
    return structured_data


def cluster_data_as_text(cluster_list, terms):
    data = []
    for cluster in cluster_list:
        data.append(terms[cluster])
    return data
