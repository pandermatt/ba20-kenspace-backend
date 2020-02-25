from cluster_analytics.word_analytics import generate_cluster

if __name__ == '__main__':
    s_data = generate_cluster()
    words = {}
    for curr in s_data:
        print("title: " + curr.text + "\ncluster: " + str(curr.cluster) + "\n")

