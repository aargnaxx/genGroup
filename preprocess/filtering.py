import os
from Bio import SeqIO, Align
from itertools import chain

DEBUG = True
DATA_DIR = '../media/'
FORMAT = 'fastq'
OUTPUT_FILE = DATA_DIR + 'processed.' + FORMAT


def read_processed():
    return SeqIO.parse(OUTPUT_FILE, FORMAT)


def pairwise_alignment_score(sequence1, sequence2):
    aligner = Align.PairwiseAligner()
    return aligner.score(sequence1, sequence2)


class Filter:
    def __init__(self, filename):
        self.readings = []
        self.files = [filename]

    def longer_than(self, filtered_length):
        self.readings = list(chain.from_iterable([
            [rec for rec in SeqIO.parse(DATA_DIR + file, FORMAT) if len(rec) > filtered_length] for file in self.files]
        ))
        return self.readings

    def exact_length(self, filtered_length):
        self.readings = list(chain.from_iterable([
            [rec for rec in SeqIO.parse(DATA_DIR + file, FORMAT) if len(rec) == filtered_length] for file in self.files]
        ))
        return self.readings


if __name__ == '__main__':
    file_list = os.listdir(DATA_DIR)
    print(file_list)
    file_list = ['J29_B_CE_IonXpress_005.fastq']

    if DEBUG:
        print(f'{len(file_list)} files found in {DATA_DIR}')
    filtered = Filter(file_list)
    # readings = filtered.longer_than(300)
    readings = filtered.exact_length(298)
    if DEBUG:
        print(f'read {len(readings)} sequences')
        print(f'dumping to {OUTPUT_FILE}')
    SeqIO.write(readings, OUTPUT_FILE, FORMAT)

