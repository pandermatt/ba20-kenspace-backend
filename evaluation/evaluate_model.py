import ast
import collections
import itertools
import math

import numpy as np
import pandas as pd

from cluster_analytics.cluster_handler import generate_cluster
from config import config


def print_cluster_probability(cluster_map):
    od = collections.OrderedDict(sorted(cluster_map.items()))
    for key, value in od.items():
        count = sum(value.values())
        elements = sorted(value.items(), key=lambda x: x[1], reverse=True)

        print(f'ClusterNr: {key}:')
        for element in elements:
            percentage = "{0:.2f}".format(element[1] / count * 100)
            print(f'        {element[0]} with {percentage}% probability')
        print('------------------------------')


def calculate_purity(cluster_id_genres_mapping, data, movie_title_genres_mapping):
    purity = 0
    n = len(data)
    for cluster_id in cluster_id_genres_mapping.keys():
        current_cluster = [d for d in data if int(d.cluster_id) == cluster_id]
        movie_classes = [np.unique(movie_title_genres_mapping[x.text]) for x in current_cluster]
        cluster_classes = list(itertools.chain.from_iterable(movie_classes))
        x = collections.Counter(cluster_classes)
        purity += (len(current_cluster) / n) * (x.most_common(1)[0][1] / len(current_cluster))
    return purity


def calculate_entropy(cluster_id_genres_mapping, data, movie_title_genres_mapping):
    entropy = 0
    n = len(data)
    for cluster_id in cluster_id_genres_mapping.keys():
        current_cluster = [d for d in data if int(d.cluster_id) == cluster_id]
        movie_classes = [np.unique(movie_title_genres_mapping[x.text]) for x in current_cluster]
        cluster_classes = list(itertools.chain.from_iterable(movie_classes))
        x = collections.Counter(cluster_classes)
        q = len(x)

        if q == 1:
            continue

        sum_clusters = 0
        n_r = len(movie_classes)
        for _, group_clusters in x.most_common():
            sum_clusters += (group_clusters / n_r) * math.log(group_clusters / n_r, 2)
        entropy += (len(current_cluster) / n) * (- (1 / math.log(q, 2)) * sum_clusters)
    return entropy


def evaluate_model():
    uuid, data = generate_cluster("MovieDb", max_iteration=10)

    path = config.input_data_file('movies_metadata.csv')
    df = pd.read_csv(path)
    df = df.fillna('')

    cluster_id_genres_mapping = {}
    movie_title_genres_mapping = {}
    for entry in data:
        result = df[df['original_title'] == entry.text]['genres'].iloc[0]
        if result == '[]':
            movie_title_genres_mapping[entry.text] = []
            continue
        genres = ast.literal_eval(result)
        movie_title_genres_mapping[entry.text] = [g['name'] for g in genres]

        for genre_map in genres:
            genre = genre_map['name']
            id_as_int = int(entry.cluster_id)
            if id_as_int in cluster_id_genres_mapping:
                m = cluster_id_genres_mapping[id_as_int]
                if genre in m:
                    m[genre] += 1
                else:
                    m[genre] = 1
            else:
                cluster_id_genres_mapping[id_as_int] = {genre: 1}
    print_cluster_probability(cluster_id_genres_mapping)

    purity = calculate_purity(cluster_id_genres_mapping, data, movie_title_genres_mapping)
    print(f"----> Purity {purity * 100}")

    entropy = calculate_entropy(cluster_id_genres_mapping, data, movie_title_genres_mapping)
    print(f"----> Entropy {entropy * 100}")


if __name__ == '__main__':
    evaluate_model()
