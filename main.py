from cluster_analytics.cluster_handler import generate_cluster

if __name__ == '__main__':
    uuid, s_data = generate_cluster(max_iteration=10)
    words = {}
    for curr in s_data:
        print(f'title: "{curr.text}" - id: {curr.cluster_id}\ncluster: {curr.terms}\n')

