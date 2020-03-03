import json
from typing import List
from typing import Tuple

from cluster_analytics.k_means_clusterer import KMeansCluster
from config import initialize_data
from file_io import ml_model_io
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster() -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data()

    log.info(f"Generating KMeans Cluster")
    k_cluster = KMeansCluster(data_handler.item_to_cluster(), 10, 10000)
    uuid = k_cluster.uuid
    log.info(f"KMeans Clustering (UUID: {uuid}) Loaded")

    ml_model_io.save_model_to_disk(k_cluster)

    log.info(f"Generating Prediction (UUID: {uuid})")
    return (
        uuid,
        prepare_clustered_data_structure(
            data_handler.display_labels(), k_cluster.get_terms_as_text()
        ),
    )


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords: str) -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data()

    k_cluster = ml_model_io.load_model_from_disk(uuid)

    if stopwords:
        log.info(f"KMeans with Stopwords {json.loads(stopwords)}")
        k_cluster.calculate(json.loads(stopwords))

    return (
        uuid,
        prepare_clustered_data_structure(
            data_handler.display_labels(), k_cluster.get_terms_as_text()
        ),
    )


def prepare_clustered_data_structure(labels, terms) -> List[ClusteredStructure]:
    return [ClusteredStructure(label, term) for label, term in zip(labels, terms)]
