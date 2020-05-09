import itertools
import json
import random
import uuid
from collections import Counter
from typing import List, Tuple

from cluster_analytics.clustered_data_structure import RestDisplayStructure, ClusterIO
from cluster_analytics.k_means_clusterer import KMeansCluster
from cluster_analytics.kensemble_clustering import KenSpaceLearning
from cluster_analytics.lda_clusterer import LDACluster
from data_import.data_handler_factory import initialize_data
from file_io import storage_io
from file_io.stopwords_io import save_stopwords
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster(selected_data, settings) -> Tuple[str, List, List]:
    data_handler = initialize_data(selected_data, settings)

    pre_load_uuid = data_handler.PRE_LOAD_UUID

    if data_handler.HAS_MULTIPLE_DATA_SOURCES:
        selected_data = data_handler.DATA_SOURCE

    if pre_load_uuid and storage_io.is_model_present(pre_load_uuid, selected_data):
        log.info(f'Preload model: {pre_load_uuid}')
        return load_cluster(data_handler.PRE_LOAD_UUID, "", selected_data, settings, data_handler=data_handler)

    return generate_k_means(data_handler, selected_data)


def generate_k_means(data_handler, selected_data, max_iteration=10000, n_clusters=None):
    documents, top_terms = data_handler.item_to_cluster(), data_handler.TOP_TERMS_PER_CLUSTER
    TOP_TERMS_PREVIEW = 4

    log.info(f'Generating KMeansCluster with {n_clusters or data_handler.calculate_n_clusters()} Clusters')
    k_cluster = KMeansCluster(documents, n_clusters or data_handler.calculate_n_clusters(), top_terms, max_iteration)

    lda_components = data_handler.calculate_n_clusters()
    if lda_components > 500:
        lda_components = 500

    log.info(f'Generating LDACluster with {lda_components} Components')
    lda_cluster = LDACluster(documents, lda_components, TOP_TERMS_PREVIEW)

    log.info(f'Generating KenSpaceLearning with {n_clusters or data_handler.calculate_n_clusters()} Clusters')
    topic_labels = KenSpaceLearning(k_cluster.get_clusters(), lda_cluster.topics()).topics_linked_to_clusters()

    cluster_uuid = str(uuid.uuid4())

    if data_handler.PRE_LOAD_UUID:
        cluster_uuid = data_handler.PRE_LOAD_UUID

    cluster_io = ClusterIO(cluster_uuid, k_cluster, lda_cluster, topic_labels)

    storage_io.save_model_to_disk(cluster_io, selected_data)

    return cluster_uuid, prepare_clustered_data_structure(data_handler, k_cluster), topic_labels


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords: str, selected_data: str, settings, data_handler=None) -> Tuple[str, List, List]:
    if not data_handler:
        data_handler = initialize_data(selected_data, settings)

    if data_handler.HAS_MULTIPLE_DATA_SOURCES:
        selected_data = data_handler.DATA_SOURCE

    cluster_io = storage_io.load_model_from_disk(uuid, selected_data)

    if stopwords:
        save_stopwords(uuid, selected_data, stopwords)
        log.info(f'KMeans with Stopwords {json.loads(stopwords)}')
        cluster_io.k_means.calculate(json.loads(stopwords))
        cluster_io.topics = KenSpaceLearning(cluster_io.k_means.get_clusters(),
                                             cluster_io.lda.topics()
                                             ).topics_linked_to_clusters()

    return uuid, prepare_clustered_data_structure(data_handler, cluster_io.k_means), cluster_io.topics


def prepare_clustered_data_structure(data_handler, k_cluster) -> List[RestDisplayStructure]:
    log.info(f'Generating Prediction')
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
