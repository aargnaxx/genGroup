import os
from Bio import SeqIO
from django.conf.global_settings import MEDIA_ROOT


def write_clustering_report_fasta(filename, sequences):
    with open(os.path.join(MEDIA_ROOT, "reports", filename), 'w') as output_file:
        SeqIO.write(sequences, output_file, 'fasta')
