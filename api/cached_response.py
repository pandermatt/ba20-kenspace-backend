import threading
from typing import List, Tuple

from api import errors
from cluster_analytics import cluster_handler
from models.clustered_data_structure import RestDisplayStructure
from util.logger import log
from util.timed_cache import timed_cache

cluster_generation_lock = threading.Lock()


def start_cluster_generation_thread(data) -> Tuple[str, List[RestDisplayStructure]]:
    log.info('Starting request: {0}'.format(threading.active_count()))
    cluster_generation_lock.acquire()
    log.info('Enter cluster generation: ID {0}'.format(threading.current_thread().ident))
    try:
        c = cached_cluster(data)
    finally:
        cluster_generation_lock.release()
    return c


@timed_cache(minutes=10)
def cached_cluster(data) -> Tuple[str, List[RestDisplayStructure]]:
    """
    Cache Cluster for 10 min
    Attention: Different user will receive the same cluster in this 'life span'
    """
    return cluster_handler.generate_cluster(data)


def extract_data_from_auth_header(auth_header):
    credentials = auth_header.split(":")
    if len(credentials) != 2:
        return errors.unauthorized_response()
    if not credentials[0].startswith("Bearer "):
        return errors.unauthorized_response()
    return credentials[1]


def generate_queries(uuid, stopwords, auth_header):
    selected_data = extract_data_from_auth_header(auth_header)
    if uuid is "":
        uuid, result = start_cluster_generation_thread(selected_data)
    else:
        uuid, result = cluster_handler.load_cluster(uuid, stopwords, selected_data)

    return {
        "uuid": uuid,
        "results": [{
            "text": cluster.text,
            "meta_info": cluster.meta_info,
            "cluster_id": cluster.cluster_id,
            "data": cluster.terms
        } for cluster in result]
    }
