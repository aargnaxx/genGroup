import json
from sklearn_extra.cluster import KMedoids
from preprocess.scoring import Scoring, calculate_affinity, calculate_dissimilarity
from sklearn.metrics import pairwise_distances
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from collections import Counter


class Clustering:
    def __init__(self, scores, reading_length, clustering_type='kmedoids', num_clusters=None):
        if clustering_type == 'spectral':
            dis = calculate_affinity(scores, reading_length)
        else:
            dis = calculate_dissimilarity(scores, reading_length)
        pd = pairwise_distances(dis)
        self.num_clusters = num_clusters
        if clustering_type == 'kmedoids':
            k_med = KMedoids(num_clusters, metric='precomputed')
            self.results = k_med.fit(pd)
            self.centers = k_med.medoid_indices_
        elif clustering_type == 'agglomerative':
            self.results = AgglomerativeClustering(num_clusters, affinity='precomputed', linkage='complete')
        elif clustering_type == 'spectral':
            self.results = SpectralClustering(num_clusters, affinity='precomputed',
                                              assign_labels='discretize', n_jobs=-1)
        if clustering_type != 'kmedoids':
            self.results.fit(pd)
            self.centers = [
                list(self.results.labels_).index(
                    next(filter(lambda x: x == i, self.results.labels_), None)
                ) for i in range(num_clusters)
            ]
        self.c = Counter(self.results.labels_)

    def print(self):
        print('count:', self.c)
        print('cluster labels:', self.results.labels_)
        print('center indices:', self.centers)

    def save_result(self):
        result = {
            'num_clusters': self.num_clusters,
            'labels': (" ".join(str(x) for x in self.results.labels_),)[0],
            'clusters_count': {i: self.c[i] for i in range(self.num_clusters)},
            'centers': (" ".join(str(x) for x in self.centers),)[0],
        }
        return result


if __name__ == '__main__':
    sc = Scoring('J29_B_CE_IonXpress_005.fastq', 298)
    sc.score_calc()
    # cl = Clustering(scores=sc.score, reading_length=298, clustering_type='kmedoids', num_clusters=3)
    # cl = Clustering(scores=sc.score, reading_length=298, clustering_type='agglomerative', num_clusters=3)
    cl = Clustering(scores=sc.score, reading_length=298, clustering_type='spectral', num_clusters=3)
    cl.print()
    print(json.dumps(cl.save_result(), indent=4))
