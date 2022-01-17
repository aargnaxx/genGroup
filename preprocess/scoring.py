import os.path
from multiprocessing import Pool
from Bio import pairwise2
from preprocess.filtering import Filter

NUM_PROCESSORS = 12
DEBUG = False


class Scoring:
    def __init__(self, file_name, reading_length=None):
        if reading_length:
            fl = Filter(file_name)
            self.records = fl.exact_length(reading_length)
            self.reading_length = reading_length
        else:
            # TODO add
            pass
        self.file_name = file_name
        self.num_recs = len(self.records)
        self.score = []

    def parallelized_score_calculation(self, rid):
        if DEBUG:
            print(f'psc with id {rid}')
        num_seqs = len(self.records)
        scores = [0 for i in range(num_seqs)]
        for j in range(num_seqs):
            scores[j] = pairwise2.align.globalxs(self.records[rid].seq, self.records[j].seq, -1, -1,
                                                 penalize_end_gaps=False, score_only=True)
        return rid, scores

    def score_calc(self):
        self.score = [[0.0 for i in range(self.num_recs)] for j in range(self.num_recs)]
        with Pool(NUM_PROCESSORS) as p:
            scores = p.map(self.parallelized_score_calculation, [i for i in range(self.num_recs)])
            for i in range(self.num_recs):
                self.score[scores[i][0]] = scores[i][1]
        return self.score

    def save_score(self):
        with open(f'{self.file_name}.{self.reading_length}.scores.txt', 'w+') as write_score:
            for i in self.score:
                line = ""
                for j in i:
                    line += str(j) + ' '
                line += '\n'
                write_score.write(line)

    def read_score(self):
        with open(f'{self.file_name}.{self.reading_length}.scores.txt', 'r') as load_score:
            content = load_score.readlines()
            for line in content:
                self.score.append([float(i) for i in line.rstrip().split(' ')])


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


def main(input_file, reading_length):
    sc = Scoring(input_file, reading_length)
    sc.score_calc()


if __name__ == "__main__":
    main('../media/files/J30_B_CE_IonXpress_006.fastq', 298)
