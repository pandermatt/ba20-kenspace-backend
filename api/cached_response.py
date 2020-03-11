import threading
from typing import List, Tuple

from cluster_analytics import cluster_handler
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.timed_cache import timed_cache

cluster_generation_lock = threading.Lock()


def start_cluster_generation_thread(data) -> Tuple[str, List[ClusteredStructure]]:
    log.info('Starting request: {0}'.format(threading.active_count()))
    cluster_generation_lock.acquire()
    log.info('Enter cluster generation: ID {0}'.format(threading.current_thread().ident))
    try:
        c = cached_cluster(data)
    finally:
        cluster_generation_lock.release()
    return c


@timed_cache(minutes=10)
def cached_cluster(data) -> Tuple[str, List[ClusteredStructure]]:
    """
    Cache Cluster for 10 min
    Attention: Different user will receive the same cluster in this 'life span'
    """
    return cluster_handler.generate_cluster(data)


def extract_data(auth_header):
    return auth_header.split(":")[-1]


def generate_queries(uuid, stopwords, auth_header):
    selected_data = extract_data(auth_header)
    if uuid is "":
        uuid, result = start_cluster_generation_thread(selected_data)
    else:
        uuid, result = cluster_handler.load_cluster(uuid, stopwords, selected_data)

    return {
        "uuid": uuid,
        "results": [{
            "text": cluster.text,
            "content": cluster.content,
            "cluster_id": cluster.cluster_id,
            "data": cluster.terms
        } for cluster in result]
    }
