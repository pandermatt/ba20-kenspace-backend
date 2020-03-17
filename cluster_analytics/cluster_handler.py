import itertools
import json
from collections import Counter
from typing import List, Tuple

from cluster_analytics.k_means_clusterer import KMeansCluster
from data_import.data_handler_factory import initialize_data
from file_io import storage_io
from models.clustered_data_structure import RestDisplayStructure
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster(selected_data) -> Tuple[str, List[RestDisplayStructure]]:
    data_handler = initialize_data(selected_data)

    return generate_k_means(data_handler, selected_data)


def generate_k_means(data_handler, selected_data, max_iteration=10000, n_clusters=None):
    log.info(f'Generating KMeans with {n_clusters or data_handler.calculate_n_clusters()} Clusters')
    k_cluster = KMeansCluster(data_handler.item_to_cluster(),
                              n_clusters or data_handler.calculate_n_clusters(),
                              data_handler.TOP_TERMS_PER_CLUSTER,
                              max_iteration)
    storage_io.save_model_to_disk(k_cluster, selected_data)

    return k_cluster.uuid, prepare_clustered_data_structure(data_handler.display_labels(),
                                                            data_handler.meta_info(),
                                                            k_cluster)


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords: str, selected_data: str) -> Tuple[str, List[RestDisplayStructure]]:
    data_handler = initialize_data(selected_data)

    k_cluster = storage_io.load_model_from_disk(uuid, selected_data)

    if stopwords:
        log.info(f'KMeans with Stopwords {json.loads(stopwords)}')
        k_cluster.calculate(json.loads(stopwords))

    return uuid, prepare_clustered_data_structure(data_handler.display_labels(), data_handler.meta_info(), k_cluster)


def prepare_clustered_data_structure(labels, meta_info, k_cluster) -> List[RestDisplayStructure]:
    log.info(f'Generating Prediction (UUID: {k_cluster.uuid})')
    return [RestDisplayStructure(label, meta_info, term, cluster_id) for label, meta_info, term, cluster_id in
            zip(labels, meta_info, remove_rare_terms(k_cluster.get_terms()), k_cluster.get_cluster_id())]


def remove_rare_terms(cluster_word_list):
    flatten_list = list(itertools.chain.from_iterable(cluster_word_list))
    filter_terms = [key for key, val in Counter(flatten_list).items() if val == 1]
    return [[k for k in cluster_word if k not in filter_terms] for cluster_word in cluster_word_list]
