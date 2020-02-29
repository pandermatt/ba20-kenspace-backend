from cluster_analytics.cluster_handler import generate_cluster

if __name__ == '__main__':
    uuid, s_data = generate_cluster()
    words = {}
    for curr in s_data:
        print("title: " + curr.text + "\ncluster: " + str(curr.cluster) + "\n")

