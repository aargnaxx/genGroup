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
        elif clustering_type == 'agglomerative':
            self.results = AgglomerativeClustering(num_clusters, affinity='precomputed', linkage='complete')
        elif clustering_type == 'spectral':
            self.results = SpectralClustering(num_clusters, affinity='precomputed',
                                              assign_labels='discretize', n_jobs=-1)
        if clustering_type != 'kmedoids':
            self.results.fit(pd)

    def print(self):
        c = Counter(self.results.labels_)
        print(c)
        print(self.results.labels_)

    def save_result(self, output_file):
        lines = str(self.num_clusters) + "\n---\n"
        lines += ", ".join(str(x) for x in self.results.labels_)
        lines += "\n---\n"
        c = Counter(self.results.labels_)
        for i in range(self.num_clusters):
            lines += f'{i}({c[i]})\n'
        with open(output_file, 'w+') as file:
            file.writelines(lines)


def main(input_file, reading_length):
    sc = Scoring(input_file, reading_length)
    sc.score_calc()
    # cl = Clustering(scores=sc.score, reading_length=reading_length, clustering_type='kmedoids', num_clusters=3)
    # cl = Clustering(scores=sc.score, reading_length=reading_length, clustering_type='agglomerative', num_clusters=3)
    cl = Clustering(scores=sc.score, reading_length=reading_length, clustering_type='spectral', num_clusters=3)
    cl.print()
    # cl.save_result('result_spec.txt')


if __name__ == "__main__":
    main('../media/files/J29_B_CE_IonXpress_005.fastq', 298)
