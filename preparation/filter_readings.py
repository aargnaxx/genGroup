import os
from Bio import SeqIO
from itertools import chain

DEBUG = True
DATA_DIR = '../jeleni/'
OUTPUT_FILE = 'processed.fastq'
FORMAT = 'fastq'


def read_processed():
    return SeqIO.parse(OUTPUT_FILE, FORMAT)


if __name__ == '__main__':
    files = os.listdir(DATA_DIR)
    if DEBUG:
        print(f'{len(files)} files found in {DATA_DIR}')
    reads = list(chain.from_iterable(
        [[rec for rec in SeqIO.parse(DATA_DIR + file, FORMAT) if len(rec) > 300] for file in files])
    )
    if DEBUG:
        print(f'read {len(reads)} sequences')
        print(f'dumping to {OUTPUT_FILE}')
    SeqIO.write(reads, OUTPUT_FILE, FORMAT)

    # for seq_record in SeqIO.parse('jelen/alela_jelen.fasta', 'fasta'):
    #     print(seq_record.id)
    #     print(repr(seq_record.seq))
    #     print(len(seq_record))
