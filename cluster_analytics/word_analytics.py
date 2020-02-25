from cluster_analytics.k_means_clusterer import KCluster
from config import initialize_data
from models.clustered_data_structure import ClusteredStructure


def generate_cluster():
    data_handler = initialize_data()

    k_cluster = KCluster(data_handler.item_to_cluster(), 10, 10000)
    return prepare_clustered_data_structure(data_handler.display_labels(), k_cluster)


def prepare_clustered_data_structure(display_labels, k_cluster):
    return [ClusteredStructure(label, feature_as_text(k_cluster.make_prediction(label), k_cluster.features))
            for label in display_labels]


def feature_as_text(cluster_list, feature):
    return [feature[cluster] for cluster in cluster_list]
