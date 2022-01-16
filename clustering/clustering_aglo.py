from preprocess.scoring import Scoring, calculate_dissimilarity
from sklearn.metrics import pairwise_distances
from sklearn.cluster import AgglomerativeClustering
from collections import Counter


class ClusteringAglo:
    def __init__(self, num_clusters, scores, reading_length):
        diss = calculate_dissimilarity(scores, reading_length)
        pd = pairwise_distances(diss)
        self.num_clusters = num_clusters
        self.aglo = AgglomerativeClustering(num_clusters, affinity='precomputed', linkage='complete')
        self.aglo.fit(pd)

    def print(self):
        print(self.aglo.labels_)

    def save_result(self, output_file):
        lines = str(self.num_clusters) + "\n---\n"
        lines += ", ".join(str(x) for x in self.aglo.labels_)
        lines += "\n---\n"
        c = Counter(self.aglo.labels_)
        print(c)
        for i in range(self.num_clusters):
            lines += f'{i}({c[i]})\n'
        with open(output_file, 'w+') as file:
            file.writelines(lines)


def main(input_file, reading_length):
    sc = Scoring(input_file, reading_length)
    sc.score_calc()
    cl = ClusteringAglo(3, sc.score, reading_length)
    cl.print()
    cl.save_result('result_aglo.txt')


if __name__ == "__main__":
    main('../media/files/J29_B_CE_IonXpress_005.fastq', 298)
