import ast
import collections
import csv
import itertools
import math

import numpy as np
import pandas as pd

from cluster_analytics.cluster_handler import generate_k_means
from config import config
from data_import.csv_data_handler import CsvDataHandler


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


def calculate_entropy(cluster_id_genres_mapping, data, movie_title_genres_mapping, all_labels=True):
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
        n_r = len(current_cluster)

        if all_labels:
            for _, group_clusters in x.most_common():
                sum_clusters += (group_clusters / n_r) * math.log(group_clusters / n_r, 2)
            entropy += (n_r / n) * (- (1 / math.log(q, 2)) * sum_clusters)
        else:
            most_common = x.most_common(1)[0][1]
            if n_r - most_common == 0:
                continue
            for p in [most_common, n_r - most_common]:
                sum_clusters += (p / n_r) * math.log(p / n_r, 2)
            entropy += (n_r / n) * (-1 * sum_clusters)
    return entropy


def evaluate_model(data, max_iterations=100):
    _, data = generate_k_means(data, 'Test Data Set', max_iterations)

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
    # print_cluster_probability(cluster_id_genres_mapping)

    purity = calculate_purity(cluster_id_genres_mapping, data, movie_title_genres_mapping)
    print(f"----> Purity {purity * 100}")

    entropy = calculate_entropy(cluster_id_genres_mapping, data, movie_title_genres_mapping)
    print(f"----> Entropy {entropy}")

    F, overall_precision, overall_recall = calculate_precision_and_overall(cluster_id_genres_mapping, data,
                                                                           movie_title_genres_mapping)
    print(f"----> Precision {overall_precision}")
    print(f"----> Recall {overall_recall}")
    print(f"----> F {F}")

    return [purity, entropy, overall_precision, overall_recall, F]


def calculate_precision_and_overall(cluster_id_genres_mapping, data, movie_title_genres_mapping):
    od = collections.OrderedDict(sorted(cluster_id_genres_mapping.items()))
    overall_precision = 0
    overall_recall = 0
    overall_count = 0
    for key, value in od.items():
        elements = sorted(value.items(), key=lambda x: x[1], reverse=True)

        items_in_cluster = [d for d in data if int(d.cluster_id) == key]
        cluster_words = [d.terms for d in items_in_cluster]
        flatten_list = list(itertools.chain.from_iterable(cluster_words))
        counter_x = collections.Counter(flatten_list)

        if not counter_x.most_common(2):
            continue

        recommend = counter_x.most_common(2)[0]
        recommend2 = [[None]]
        we_recommend = recommend[1]
        if len(counter_x.most_common(2)) > 1:
            recommend2 = counter_x.most_common(2)[1]
            we_recommend += recommend2[1]

        element = elements[0]
        element2 = [[None]]
        all_relevant = element[1]
        if len(elements) > 1:
            element2 = elements[1]
            all_relevant += element2[1]

        correct_recommended = 0
        for item in items_in_cluster:
            if ((recommend[0] in item.terms or recommend2[0] in item.terms) and
                    (element[0] in movie_title_genres_mapping[item.text]
                     or element2[0] in movie_title_genres_mapping[item.text])):
                correct_recommended += 1
        overall_precision += correct_recommended / we_recommend
        overall_recall += correct_recommended / all_relevant
        overall_count += 1
    overall_precision = overall_precision / overall_count
    overall_recall = overall_recall / overall_count

    # Precision
    # P = relevant recommendation / items we recommend
    # Recall
    # R = relevant recommendation / all relevant items
    # Precision is the fraction of recommended items that is actually relevant to the user,
    # Recall can be defined as the fraction of relevant items that are also part of the set of recommended items

    F = (2 * overall_precision * overall_recall) / (overall_precision + overall_recall)
    return F, overall_precision, overall_recall


class TestDbHandler(CsvDataHandler):
    def __init__(self, clean_up_method='nltk'):
        CsvDataHandler.__init__(self, 'MovieDB', 'movies_metadata.csv')
        self.df = self.df.sample(4000)
        self.n_clusters = None
        self.saved_item_to_cluster = [i + j for i, j in
                                      zip(self.clean_up_df_text('overview', clean_up_method=clean_up_method),
                                          self.clean_up_df_text('original_title', clean_up_method=clean_up_method))]

    def display_labels(self):
        return self.df['original_title'].tolist()

    def calculate_n_clusters(self):
        return self.n_clusters


def save_results(fields):
    with open(r'result.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        f.flush()


if __name__ == '__main__':
    """
    In this method, you can Run checks with your customisations:
    """

    config.SAVE_TO_FILE = False

    save_results(["min_df", "Purity", "Entropy", "Precision", "Recall", "F-Score"])

    # count = 5
    # for j in range(100):
    #     a = np.zeros([count, 6])
    #     for i in range(count):
    #         handler.TOP_TERMS_PER_CLUSTER = ((j + 1) * 5)
    #         a[i, :] = [(j + 1) * 5] + evaluate_model(handler)
    #     save_results(np.mean(a, axis=0))

    # count = 5
    # handler.TOP_TERMS_PER_CLUSTER = 50
    # for j in range(50):
    #     a = np.zeros([count, 6])
    #     for i in range(count):
    #         handler.n_clusters = ((j + 1) * 20)
    #         a[i, :] = [(j + 1) * 20] + evaluate_model(handler)
    #     save_results(np.mean(a, axis=0))

    handler = TestDbHandler()
    handler.TOP_TERMS_PER_CLUSTER = 15
    handler.n_clusters = 100
    for i in range(10):
        save_results([0.2] + evaluate_model(handler))

    # for i in range(10):
    #     handler = TestDbHandler(clean_up_method='spacy')
    #     handler.TOP_TERMS_PER_CLUSTER = 20
    #     handler.n_clusters = 400
    #     save_results(['spaCy'] + evaluate_model(handler))

    # save_results(["purity", "entropy", "overall_precision", "overall_recall", "F"])
    #
    # handler = TestDbHandler()
    # for i in range(50):
    #     save_results(evaluate_model(handler))
