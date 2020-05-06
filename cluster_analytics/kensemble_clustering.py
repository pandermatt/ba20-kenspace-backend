from cluster_analytics.clustered_data_structure import RestDisplayStructureKenSemble


class KenSpaceLearning:
    """
    combines kmeans and lda
    """

    def __init__(self, k_means_clusters, lda_topics):
        self.k_means_clusters = k_means_clusters
        self.lda_topics = lda_topics

    def topics_linked_to_clusters(self):
        merged_list = []
        for i, k_current in enumerate(self.k_means_clusters):
            res_ind_lda = None
            max_sim = -1
            for l_current in self.lda_topics:
                similarity = self.__similarity(k_current, l_current)
                index_l = self.lda_topics.index(l_current)
                if similarity > max_sim:
                    res_ind_lda = index_l
                    max_sim = similarity
            tmp_topic = self.lda_topics[res_ind_lda]
            # get top 3 from topic
            top_three = []
            for j, current in enumerate(tmp_topic):
                if j == 3:
                    break
                else:
                    top_three.append(current)
            merged_list.append(RestDisplayStructureKenSemble(top_three, i))
        return merged_list

    @staticmethod
    def __similarity(k_current, l_current):
        hits = 0
        for k_element in k_current:
            if k_element in l_current:
                hits = hits + 1
        return hits / len(k_current)
