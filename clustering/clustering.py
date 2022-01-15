from preprocess.scoring import Scoring, pcoa_calculate_dissimilarity
from sklearn.metrics import pairwise_distances
from sklearn_extra.cluster import KMedoids
from collections import Counter


class ClusteringKm:
    def __init__(self, num_clusters, scores, reading_length):
        diss = pcoa_calculate_dissimilarity(scores, reading_length)
        pd = pairwise_distances(diss)
        self.num_clusters = num_clusters
        self.kmedoids = KMedoids(num_clusters, metric='precomputed')
        # self.results = KMedoids.get_params(self.kmedoids)
        self.results = self.kmedoids.fit(pd)

    def print(self):
        print(self.results)
        print(self.results.labels_)
        # print(self.kmedoids.cluster_centers_)

    def save_result(self, output_file):
        lines = str(self.num_clusters) + "\n---\n"
        lines += ", ".join(str(x) for x in self.results.labels_)
        lines += "\n---\n"
        c = Counter(self.results.labels_)
        print(c)
        for i in range(self.num_clusters):
            lines += f'{i}({c[i]})\n'
        with open(output_file, 'w+') as file:
            file.writelines(lines)


def main(input_file, reading_length):
    sc = Scoring(input_file, reading_length)
    sc.score_calc()
    cl = ClusteringKm(3, sc.score, reading_length)
    cl.print()
    cl.save_result('result.txt')


if __name__ == "__main__":
    main('../media/files/J29_B_CE_IonXpress_005.fastq', 298)
