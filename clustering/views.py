import os

from django.shortcuts import render

from Bio import SeqIO, SeqRecord

from genGroup.settings import MEDIA_ROOT

# Create your views here.


def run(request, seq_length):
    file = request.session.get('files')
    with open(os.path.join(MEDIA_ROOT, file)) as f:
        sequences = filter_out(f, seq_length)

    return render(request, 'clustering/index.html', {"sequences": sequences})


def filter_out(fastqfile, seq_len):
    filtered_records = []
    for record in SeqIO.parse(fastqfile, "fastq"):
        if len(record.seq) == seq_len:
            filtered_records.append(record.seq)

    return filtered_records
