import itertools
import json
import random
from collections import Counter
from typing import List, Tuple

from cluster_analytics.k_means_clusterer import KMeansCluster
from data_import.data_handler_factory import initialize_data
from file_io import storage_io
from file_io.stopwords_io import save_stopwords
from models.clustered_data_structure import RestDisplayStructure
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster(selected_data, settings) -> Tuple[str, List[RestDisplayStructure]]:
    data_handler = initialize_data(selected_data, settings)

    pre_load_uuid = data_handler.PRE_LOAD_UUID
    if pre_load_uuid and storage_io.is_model_present(pre_load_uuid, selected_data):
        log.info(f'Preload model: {pre_load_uuid}')
        return load_cluster(data_handler.PRE_LOAD_UUID, "", selected_data, settings)

    return generate_k_means(data_handler, selected_data)


def generate_k_means(data_handler, selected_data, max_iteration=10000, n_clusters=None):
    log.info(f'Generating KMeans with {n_clusters or data_handler.calculate_n_clusters()} Clusters')
    k_cluster = KMeansCluster(data_handler.item_to_cluster(),
                              n_clusters or data_handler.calculate_n_clusters(),
                              data_handler.TOP_TERMS_PER_CLUSTER,
                              max_iteration)

    if data_handler.PRE_LOAD_UUID:
        k_cluster.uuid = data_handler.PRE_LOAD_UUID

    storage_io.save_model_to_disk(k_cluster, selected_data)

    return k_cluster.uuid, prepare_clustered_data_structure(data_handler, k_cluster)


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords: str, selected_data: str, settings) -> Tuple[str, List[RestDisplayStructure]]:
    data_handler = initialize_data(selected_data, settings)

    k_cluster = storage_io.load_model_from_disk(uuid, selected_data)

    if stopwords:
        save_stopwords(uuid, selected_data, stopwords)
        log.info(f'KMeans with Stopwords {json.loads(stopwords)}')
        k_cluster.calculate(json.loads(stopwords))

    return uuid, prepare_clustered_data_structure(data_handler, k_cluster)


def prepare_clustered_data_structure(data_handler, k_cluster) -> List[RestDisplayStructure]:
    log.info(f'Generating Prediction (UUID: {k_cluster.uuid})')
    result = [RestDisplayStructure(label, meta_info, term, cluster_id)
              for label, meta_info, term, cluster_id in
              zip(data_handler.display_labels(),
                  data_handler.meta_info(),
                  remove_rare_terms(k_cluster.get_terms()),
                  k_cluster.get_cluster_id())]

    if data_handler.SHUFFLE_DATA:
        random.shuffle(result)
    return result


def remove_rare_terms(cluster_word_list):
    flatten_list = list(itertools.chain.from_iterable(cluster_word_list))
    filter_terms_set = set([key for key, val in Counter(flatten_list).items() if val == 1])
    return [[k for k in cluster_word if k not in filter_terms_set] for cluster_word in cluster_word_list]
