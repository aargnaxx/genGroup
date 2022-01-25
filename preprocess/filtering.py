import os
from itertools import chain
from Bio import SeqIO, Align
from genGroup.settings import MEDIA_ROOT

DEBUG = False
FORMAT = 'fastq'
OUTPUT_FILE = MEDIA_ROOT + 'processed.' + FORMAT


class Filter:
    def __init__(self, filename, format_="fastq"):
        self.readings = []
        self.files = [filename]
        self.format = format_

    def cond(self, f):
        self.readings = list(chain.from_iterable(
            [[rec for rec in SeqIO.parse(os.path.join(MEDIA_ROOT, "files", file), self.format)
              if f(rec)] for file in self.files]
        ))
        if DEBUG:
            print(f'read {len(self.readings)} sequences')
        return self.readings

    def longer_than(self, filtered_length):
        if DEBUG:
            print(f'length longer than {filtered_length}')
        return self.cond(lambda x: len(x.seq) > filtered_length)

    def exact_length(self, filtered_length):
        if DEBUG:
            print(f'length {filtered_length}')
        return self.cond(lambda x: len(x.seq) == filtered_length)

    def length_between(self, filtered_length):
        if DEBUG:
            print(f'min {min(filtered_length) + 1}, max {max(filtered_length) + 1}')
        return self.cond(lambda x: (min(filtered_length) < len(x.seq) < max(filtered_length)))

    # TODO maybe add trimming edges


if __name__ == '__main__':
    file_ = 'J29_B_CE_IonXpress_005.fastq'
    filtered = Filter(file_)
    readings = filtered.exact_length(298)
    print('example seq:')
    print(readings[0].seq)
