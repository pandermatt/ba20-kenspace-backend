from util.timed_cache import timed_cache
from word_analytics.word_analytics import generate_cluster


@timed_cache(minutes=10)
def cached_cluster():
    return generate_cluster()


@timed_cache(minutes=10)
def generate_queries():
    return {"results":
        [{
            "text": cluster.text,
            "data": cluster.cluster
        } for cluster in cached_cluster()]
    }


@timed_cache(minutes=10)
def generate_facet():
    words = {}
    for curr in cached_cluster():
        for i in curr.cluster:
            if i in words:
                words[i] = words[i] + 1
            else:
                words[i] = 1
    return {"results": sorted(words.items(), key=lambda kv: kv[1], reverse=True)}
