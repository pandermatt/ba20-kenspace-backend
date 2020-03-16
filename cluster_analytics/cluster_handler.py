import itertools
import json
from collections import Counter
from typing import List, Tuple

from cluster_analytics.k_means_clusterer import KMeansCluster
from data_import.data_handler_factory import initialize_data
from file_io import storage_io
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster(selected_data, max_iteration=10000) -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data(selected_data)

    log.info(f'Generating KMeans with {data_handler.calculate_n_clusters()} Clusters')
    k_cluster = KMeansCluster(data_handler.item_to_cluster(),
                              data_handler.calculate_n_clusters(),
                              data_handler.TOP_TERMS_PER_CLUSTER,
                              max_iteration)
    uuid = k_cluster.uuid
    log.info(f'KMeans Clustering (UUID: {uuid}) Loaded')

    storage_io.save_model_to_disk(k_cluster, selected_data)

    log.info(f'Generating Prediction (UUID: {uuid})')

    terms = remove_rare_terms(k_cluster.get_terms())
    return uuid, prepare_clustered_data_structure(data_handler.display_labels(), terms, k_cluster.get_cluster_id())


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords: str, selected_data: str) -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data(selected_data)

    k_cluster = storage_io.load_model_from_disk(uuid, selected_data)

    if stopwords:
        log.info(f'KMeans with Stopwords {json.loads(stopwords)}')
        k_cluster.calculate(json.loads(stopwords))

    terms = remove_rare_terms(k_cluster.get_terms())
    return uuid, prepare_clustered_data_structure(data_handler.display_labels(), terms, k_cluster.get_cluster_id())


def prepare_clustered_data_structure(labels, terms, cluster_ids) -> List[ClusteredStructure]:
    return [ClusteredStructure(label, term, str(cluster_id)) for label, term, cluster_id in
            zip(labels, terms, cluster_ids)]


def remove_rare_terms(cluster_word_list):
    flatten_list = list(itertools.chain.from_iterable(cluster_word_list))
    filter_terms = [key for key, val in Counter(flatten_list).items() if val == 1]
    return [[k for k in cluster_word if k not in filter_terms] for cluster_word in cluster_word_list]
