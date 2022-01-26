from multiprocessing import Pool
from Bio import pairwise2
from preprocess.filtering import Filter
import numpy as np

NUM_PROCESSORS = 4
DEBUG = False


class Scoring:
    def __init__(self, file_name, reading_length=None):
        if reading_length:
            fl = Filter(file_name)
            self.records = fl.exact_length(reading_length)
            self.sequences = []
            for i in range(len(self.records)):
                self.sequences.append(str(self.records[i].seq))
            self.reading_length = reading_length
        self.file_name = file_name
        self.num_recs = len(self.records)
        self.score = np.zeros((self.num_recs, self.num_recs))

    def parallelized_score_calculation(self, rid):
        if DEBUG:
            print(f'parallelized_score_calculation with id {rid}')
        score = [[0 for _ in range(self.num_recs)] for _ in range(self.num_recs)]
        score[rid][rid] = self.reading_length
        for j in range(rid + 1, self.num_recs):
            p_score = int(pairwise2.align.globalxs(self.records[rid].seq, self.records[j].seq, -1, -1,
                                                   penalize_end_gaps=False, score_only=True))
            score[rid][j] = p_score
            score[j][rid] = p_score
        return score

    def score_calc(self):
        with Pool(NUM_PROCESSORS) as p:
            parallel = p.map(self.parallelized_score_calculation, [i for i in range(self.num_recs)])
            for i in parallel:
                self.score += i
        return self.score


def calculate_dissimilarity(scores, reading_len):
    for i in range(len(scores)):
        for j in range(len(scores)):
            scores[i][j] = - (scores[i][j] / reading_len - 1)
    return scores


def calculate_affinity(scores, reading_len):
    for i in range(len(scores)):
        for j in range(len(scores)):
            scores[i][j] = scores[i][j] / reading_len
    return scores


if __name__ == "__main__":
    sc = Scoring('J30_B_CE_IonXpress_006.fastq', 298)
    sc.score_calc()
    print(sc.score[0][:25])
    print(sc.score.transpose()[0][:25])
