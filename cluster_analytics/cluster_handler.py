import json
from typing import List, Tuple

from cluster_analytics.k_means_clusterer import KMeansCluster
from config import initialize_data
from file_io import ml_model_io
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster() -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data()

    k_cluster = KMeansCluster(data_handler.item_to_cluster(), 10, 10000)
    uuid = k_cluster.uuid
    log.info(f'KMeans Clustering (UUID: {uuid}) Loaded')

    ml_model_io.save_model_to_disk(k_cluster)

    return uuid, prepare_clustered_data_structure(data_handler.content_labels(),
                                                  data_handler.display_labels(),
                                                  k_cluster)


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords) -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data()

    k_cluster = ml_model_io.load_model_from_disk(uuid)

    if stopwords:
        print(json.loads(stopwords))
        k_cluster.calculate(json.loads(stopwords))

    return uuid, prepare_clustered_data_structure(data_handler.content_labels(),
                                                  data_handler.display_labels(),
                                                  k_cluster)


def prepare_clustered_data_structure(content_labels, display_labels, k_cluster):
    return [
        ClusteredStructure(display_label, k_cluster.make_prediction_as_text(label))
        for label, display_label in zip(content_labels, display_labels)
    ]
