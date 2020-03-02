import json
from typing import List, Tuple

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from cluster_analytics.k_means_clusterer import KMeansCluster
from config import initialize_data
from data_import.data_handler import DataHandler
from file_io import ml_model_io
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.timed_cache import timed_cache


def generate_cluster() -> Tuple[str, List[ClusteredStructure]]:
    data_handler = initialize_data()

    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(" ".join(data_handler.item_to_cluster()))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    log.info(f'Generating KMeans Cluster')
    k_cluster = KMeansCluster(data_handler.item_to_cluster(), 10, 10000)
    uuid = k_cluster.uuid
    log.info(f'KMeans Clustering (UUID: {uuid}) Loaded')

    ml_model_io.save_model_to_disk(k_cluster)

    log.info(f'Generating Prediction (UUID: {uuid})')
    return uuid, prepare_clustered_data_structure(data_handler, k_cluster)


@timed_cache(minutes=100)
def load_cluster(uuid: str, stopwords: str) -> Tuple[str, List[ClusteredStructure]]:
    k_cluster = ml_model_io.load_model_from_disk(uuid)

    if stopwords:
        log.info(f'KMeans with Stopwords {json.loads(stopwords)}')
        k_cluster.calculate(json.loads(stopwords))

    return uuid, prepare_clustered_data_structure(initialize_data(), k_cluster)


def prepare_clustered_data_structure(data_handler: DataHandler, k_cluster: KMeansCluster) -> List[ClusteredStructure]:
    return [
        ClusteredStructure(display_label, k_cluster.make_prediction_as_text(label))
        for label, display_label in zip(data_handler.content_labels(), data_handler.display_labels())
    ]
