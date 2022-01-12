import os

from django.shortcuts import render

from Bio import SeqIO

from genGroup.settings import MEDIA_ROOT

# Create your views here.


def run(request, seq_length, decrement_range, increment_range):
    file = request.session.get('files')
    seq_range = range(seq_length-decrement_range, seq_length+increment_range+1)
    with open(os.path.join(MEDIA_ROOT, file)) as f:
        sequences = filter_out(f, seq_range)

    return render(request, 'clustering/index.html', {"sequences": sequences})


def filter_out(fastqfile, seq_range):
    filtered_records = []
    for record in SeqIO.parse(fastqfile, "fastq"):
        if len(record.seq) in seq_range:
            filtered_records.append(record.seq)

    return filtered_records
