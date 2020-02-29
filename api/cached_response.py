import threading
from typing import List, Tuple

from cluster_analytics import cluster_handler
from models.clustered_data_structure import ClusteredStructure
from util.logger import log
from util.timed_cache import timed_cache

cluster_generation_lock = threading.Lock()


def start_cluster_generation_thread() -> Tuple[str, List[ClusteredStructure]]:
    log.info('Starting request: {0}'.format(threading.active_count()))
    cluster_generation_lock.acquire()
    log.info('Enter cluster generation: ID {0}'.format(threading.current_thread().ident))
    try:
        c = cached_cluster()
    finally:
        cluster_generation_lock.release()
    return c


@timed_cache(minutes=10)
def cached_cluster() -> Tuple[str, List[ClusteredStructure]]:
    """
    Cache Cluster for 10 min
    Attention: Different user will receive the same cluster in this 'life span'
    """
    return cluster_handler.generate_cluster()


def generate_queries(uuid, stopwords):
    if uuid is None:
        uuid, result = start_cluster_generation_thread()
    else:
        uuid, result = cluster_handler.load_cluster(uuid,stopwords)

    return {
        "uuid": uuid,
        "results": [{
            "text": cluster.text,
            "data": cluster.cluster
        } for cluster in result]
    }


def generate_facet(uuid):
    if uuid is None:
        _, result = start_cluster_generation_thread()
    else:
        _, result = cluster_handler.load_cluster(uuid)

    words = {}
    for curr in result:
        for i in curr.cluster:
            if i in words:
                words[i] = words[i] + 1
            else:
                words[i] = 1
    return {"results": sorted(words.items(), key=lambda kv: kv[1], reverse=True)}
