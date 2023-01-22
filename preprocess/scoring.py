import os
import time
import numpy as np
from collections import Counter
from multiprocessing import Pool
from Bio import pairwise2
from preprocess.filtering import Filter
from csv import reader, writer

NUM_PROCESSORS = 12
DEBUG = True
DATA_LOCATION = 'C:/Users/S/genGroup/media/processed/'


class Scoring:
    def __init__(self, file_name, reading_length=None, filter_unique=True):
        # if reading_length:
        fl = Filter(file_name)
        self.records = fl.exact_length(reading_length)
        self.filter_unique = filter_unique
        self.unique = dict(sorted(Counter([reading.seq for reading in self.records]).items(), key=lambda x: -x[1]))
        self.sequences = {}
        for i in range(len(self.records)):
            self.sequences[i] = self.records[i].seq
        self.reading_length = reading_length
        self.file_name = file_name
        self.num_recs = len(self.records if not filter_unique else self.unique)
        # self.save_unique()
        self.score = np.zeros((len(self.records), len(self.records)), dtype=np.short)
        # self.mini_score = np.zeros((len(self.unique), len(self.unique)), dtype=np.short)
        if DEBUG:
            print(f'{len(self.unique)} unique readings')
            print(f'{len(self.records)} total readings')

    def parallelized_score_calculation(self, rid):
        if DEBUG:
            print(f'parallelized_score_calculation with id {rid}')
        if rid == self.num_recs:
            return np.zeros((1,))
        score = np.zeros((self.num_recs - rid - 1,), dtype=np.short)
        for j in range(rid + 1, self.num_recs):
            score[j - rid - 1] = int(pairwise2.align.globalxs(self.records[rid].seq, self.records[j].seq, -1, -1,
                                                              penalize_end_gaps=False, score_only=True))
        return score

    def score_calc(self):
        if try_load_csv(self.score, self.file_name, [self.reading_length]):
            return self.score
        for x in range(0, self.num_recs, NUM_PROCESSORS):
            with Pool(NUM_PROCESSORS) as p:
                enum = enumerate(p.map(self.parallelized_score_calculation,
                                       [i for i in
                                        (range(x, x + NUM_PROCESSORS) if x < self.num_recs - NUM_PROCESSORS
                                         else range(x, self.num_recs - 1))]))
                for i, score in enum:
                    a = np.zeros((len(self.records),), dtype=np.short)
                    a[x + i + 1:x + i + 1 + len(score)] = score
                    self.score[x + i] = a
                self.score += self.score.T
                self.score += np.eye(len(self.score), dtype=np.short) * self.reading_length
        if self.filter_unique:
            self.score = multiply_scores(self.unique, self.score, len(self.records))
        save_csv(self.score, self.file_name, [self.reading_length])
        return self.score

    def save_unique(self):
        with open(DATA_LOCATION + self.file_name + 'unique.txt', 'w') as file:
            file.writelines([f'{str(i[0])} {i[1]}\n' for i in self.unique.items()])


def multiply_scores(unique, score, size):
    tra_count = 0
    for k, val in enumerate(unique.items()):
        for _ in range(val[1] - 1):
            score[len(unique) + tra_count, :] = score[k, :]
            score[:, len(unique) + tra_count] = score[:, k]
            tra_count += 1
    e = np.eye(size, dtype=np.short)
    r_l = score[0][0]
    score -= e * score
    score += e * r_l
    return score


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


def try_load_csv(data, filename, params=None):
    try:
        _filename = f'{DATA_LOCATION + filename}.{".".join(str(i) for i in params) + "." if params else ""}score.csv'
        with open(_filename, 'r') as csvfile:
            r = reader(csvfile)
            for i, row in enumerate(r):
                if len(row) > 0:
                    data[i] = row
        if DEBUG:
            print(f'successfully read csv with {len(data)} rows')
            print(data)
        return True
    except OSError as err:
        if DEBUG:
            print(err)
            print('Could not open file')
        return False


def save_csv(data, filename, params=None):
    try:
        _filename = f'{DATA_LOCATION + filename}.{".".join(str(i) for i in params) + "." if params else ""}score.csv'
        with open(_filename, 'w', newline='') as csvfile:
            w = writer(csvfile)
            for row in data:
                w.writerow(row)
        if DEBUG:
            print(f'successfully written csv with {len(data)} rows')
        return True
    except OSError as err:
        if DEBUG:
            print(err)
            print('Could not open file')
        return False


def scan_dir(path):
    files = [f for f in os.listdir(path)]
    return files


if __name__ == "__main__":
    from filtering import MEDIA_ROOT
    timer = time.time()
    times = [timer]
    for m in scan_dir(MEDIA_ROOT)[19:]:
        sc = Scoring(m, 194, True)
        # sc = Scoring(m, 201, True)
        sc.score_calc()
        times.append(time.time() - times[-1])
    executionTime = (time.time() - timer)
    print('Execution time in seconds: ' + str(executionTime))
    times.pop(0)
    print(f'Average time {sum(times) / len(times)}')
    print(f'Max time {max(times)}')
    print(f'Min time {min(times)}')
