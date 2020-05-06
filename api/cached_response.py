import threading
from typing import List, Tuple

from api import errors
from cluster_analytics import cluster_handler
from util.logger import log
from util.timed_cache import timed_cache

cluster_generation_lock = threading.Lock()


def start_cluster_generation_thread(data, settings) -> Tuple[str, List, List]:
    log.info('Starting request: {0}'.format(threading.active_count()))
    cluster_generation_lock.acquire()
    log.info('Enter cluster generation: ID {0}'.format(threading.current_thread().ident))
    try:
        c = cached_cluster(data, settings)
    finally:
        cluster_generation_lock.release()
    return c


@timed_cache(minutes=10)
def cached_cluster(data, settings) -> Tuple[str, List, List]:
    """
    Cache Cluster for 10 min
    Attention: Different user will receive the same cluster in this 'life span'
    """
    return cluster_handler.generate_cluster(data, settings)


def extract_data_from_auth_header(auth_header):
    credentials = auth_header.split(":")
    if len(credentials) != 2:
        return errors.unauthorized_response()
    if not credentials[0].startswith("Bearer "):
        return errors.unauthorized_response()
    return credentials[1]


def generate_queries(uuid, stopwords, auth_header, settings):
    selected_data = extract_data_from_auth_header(auth_header)
    if uuid is "":
        uuid, result, topic = start_cluster_generation_thread(selected_data, settings)
    else:
        uuid, result, topic = cluster_handler.load_cluster(uuid, stopwords, selected_data, settings)

    results = [{
        "text": cluster.text,
        "meta_info": cluster.meta_info,
        "cluster_id": cluster.cluster_id,
        "data": cluster.terms
    } for cluster in result]

    topics = [{
        "cluster_id": cluster.cluster_id,
        "data": cluster.terms
    } for cluster in topic]

    return {
        "uuid": uuid,
        "results": results,
        "topics": topics
    }
