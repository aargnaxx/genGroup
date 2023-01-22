import json
from sklearn_extra.cluster import KMedoids
from preprocess.scoring import Scoring, calculate_affinity, calculate_dissimilarity, DATA_LOCATION, DEBUG
from sklearn.metrics import pairwise_distances
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from collections import Counter


class Clustering:
    def __init__(self, scores, reading_length, clustering_type='kmedoids', num_clusters=None):
        if clustering_type == 'spectral':
            dis = calculate_affinity(scores, reading_length)
        else:
            dis = calculate_dissimilarity(scores, reading_length)
        print('calculating distances')
        pd = pairwise_distances(dis)
        self.num_clusters = num_clusters
        print('doing clustering')
        if clustering_type == 'kmedoids':
            k_med = KMedoids(num_clusters, metric='precomputed')
            self.results = k_med.fit(pd)
            self.centers = k_med.medoid_indices_
        elif clustering_type == 'agglomerative':
            self.results = AgglomerativeClustering(num_clusters, affinity='precomputed', linkage='complete')
        elif clustering_type == 'spectral':
            self.results = SpectralClustering(num_clusters, affinity='precomputed',
                                              assign_labels='discretize', n_jobs=4)
        if clustering_type != 'kmedoids':
            self.results.fit(pd)
            # TODO check
            self.centers = [list(self.results.labels_).index(i) for i in range(num_clusters)]
        print('clustering done, counting')
        self.c = Counter(self.results.labels_)

    def print(self):
        print('count:', self.c)
        print('cluster labels:', self.results.labels_)
        print('center indices:', self.centers)

    def return_result(self):
        result = {
            'num_clusters': f'{self.num_clusters}',
            'labels': (" ".join(str(x) for x in self.results.labels_),)[0],
            'clusters_count': {i: self.c[i] for i in range(self.num_clusters)},
            'centers': (" ".join(str(x) for x in self.centers),)[0],
        }
        return result


def run_clustering(files, clustering_type, reading_length=201, num_clusters=10):
    for file in files:
        for c in clustering_type:
            print(file)
            if read_results_json(file, [c, reading_length, num_clusters]):
                continue
            sc = Scoring(file, reading_length)
            sc.score_calc()
            print('now doing clustering')
            cl = Clustering(scores=sc.score, reading_length=reading_length,
                            clustering_type=c, num_clusters=num_clusters)
            cl.print()
            print(json.dumps(cl.return_result(), indent=4))
            save_result_json(cl.return_result(), file, [c, reading_length, num_clusters])


def read_results_json(filename, params=None):
    try:
        _filename = f'{DATA_LOCATION + filename}.{".".join(str(i) for i in params) + "." if params else ""}result.csv'
        with open(_filename, 'r') as input_file:
            data = json.load(input_file)
            if DEBUG:
                print(f'successfully read json with {len(data)} entries')
            return data
    except OSError as err:
        if DEBUG:
            print(err)
            print('Could not open file')
        return False


def save_result_json(data, filename, params=None):
    try:
        _filename = f'{DATA_LOCATION + filename}.{".".join(str(i) for i in params) + "." if params else ""}result.csv'
        with open(_filename, 'w', newline='') as output_file:
            json.dump(data, output_file)
        if DEBUG:
            print(f'successfully written json with {len(data)} entries')
        return True
    except OSError as err:
        if DEBUG:
            print(err)
            print('Could not open file')
        return False


if __name__ == '__main__':
    from file_lists import files_dqb, drb_more_than_2, drb_more_than_3

    # file_list = files_dqb
    file_list = drb_more_than_2
    # file_list = drb_more_than_3
    # file_list = ['005_S5_L001_CS1A-URS_DRB.extendedFrags_filtered.fastq', ]
    clustering_types = [
        'kmedoids',
        'agglomerative',
        # 'spectral',
    ]
    # run_clustering(file_list, clustering_types, 201, 10)
    run_clustering(file_list, clustering_types, 194, 10)
    # run_clustering(file_list, clustering_types, 201, 10)

# TODO process dump
