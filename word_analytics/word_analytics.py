import pandas as pd

from config import config
from util.noun_extraction import extract_nouns
from word_analytics.clustered_data_structure import ClusteredStructure
from word_analytics.k_means_clusterer import KCluster


def generate_cluster():
    path = config.data_file('imdb-f.csv')
    df = pd.read_csv(path)

    all_titles = get_column(df, 'movie-title')
    extracted_nouns = extract_nouns(df, 'movie-content')

    print(len(all_titles))
    print(len(extracted_nouns))

    k_cluster = KCluster(extracted_nouns, 10, 10000)
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
