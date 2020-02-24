import threading

from util.logger import log
from util.timed_cache import timed_cache
from word_analytics.word_analytics import generate_cluster

cluster_generation_lock = threading.Lock()


def start_thread():
    log.info('Starting request: {0}'.format(threading.active_count()))
    cluster_generation_lock.acquire()
    log.info('Enter cluster generation')
    try:
        c = cached_cluster()
    finally:
        cluster_generation_lock.release()
    return c


@timed_cache(minutes=10)
def cached_cluster():
    return generate_cluster()


@timed_cache(minutes=1)
def generate_queries():
    return {"results":
        [{
            "text": cluster.text,
            "data": cluster.cluster
        } for cluster in start_thread()]
    }


@timed_cache(minutes=1)
def generate_facet():
    words = {}
    for curr in start_thread():
        for i in curr.cluster:
            if i in words:
                words[i] = words[i] + 1
            else:
                words[i] = 1
    return {"results": sorted(words.items(), key=lambda kv: kv[1], reverse=True)}
