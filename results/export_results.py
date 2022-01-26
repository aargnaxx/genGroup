import os

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def write_clustering_report_fasta(filepath, sequences):
    records = (SeqRecord(Seq(seq), str(index)) for index,seq in enumerate(sequences) )
    SeqIO.write(records, filepath, 'fasta')
