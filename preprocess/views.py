import os

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from Bio import SeqIO, pairwise2

from genGroup.settings import MEDIA_ROOT

from .forms import SelectFileForm, SelectSequenceLength, UploadFileForm


# Shows up when user goes to '/preprocess/'.
def select_file(request):
    if request.method == 'POST':
        form = SelectFileForm(request.POST)
        if form.is_valid():
            request.session['file_for_analysis'] = request.POST['file_for_analysis']
            request.session['result_file'] = request.POST['result_file']
            return HttpResponseRedirect('results')

    form = SelectFileForm()
    return render(request, 'preprocess/index.html', {'form': form})


def preprocess_results(request):
    if request.method == 'POST':
        seq_lengths = request.session.get('sequence_lengths')
        form = SelectSequenceLength(
            given_choices=seq_lengths, data=request.POST)
        if form.is_valid():
            chosen_seq_length = form.cleaned_data['sequence_length']
            chosen_inc_length = form.cleaned_data['inc_offset']
            chosen_dec_length = form.cleaned_data['dec_offset']

            return redirect('clustering:run', seq_length=chosen_seq_length, decrement_range=chosen_dec_length, increment_range=chosen_inc_length)

    file_for_analysis = request.session.get('file_for_analysis')
    result_file = request.session.get('result_file')
    with open(os.path.join(MEDIA_ROOT, file_for_analysis)) as fastqfile:
        with open(os.path.join(MEDIA_ROOT, result_file)) as fastafile:
            sequence_data = preprocess(fastqfile)
            results_distances = calculate_distances_between_results(fastafile)

            fastqfile.seek(0)
            fastafile.seek(0)
            distances = calculate_distances(fastafile, fastqfile)

    sequence_data = dict(
        sorted(sequence_data.items(), key=lambda item: item[1], reverse=True))

    results_distances = dict(sorted(results_distances.items()))

    sorted_sequence_lengths = sorted(sequence_data.keys(), reverse=True)
    request.session['sequence_lengths'] = sorted_sequence_lengths

    form = SelectSequenceLength(sorted_sequence_lengths)

    context = {'form': form, 'result': sequence_data, 'results_distances': results_distances, 'distances': distances}
    return render(request, 'preprocess/preprocess_results.html', context)


def preprocess(fastqfile):
    counts = {}
    for record in SeqIO.parse(fastqfile, "fastq"):
        seq_len = len(record.seq)

        if not counts.get(seq_len):
            counts[seq_len] = 0

        counts[seq_len] += 1

    return counts

def calculate_distances_between_results(fastafile):
    distances = {}


    records = []
    for record in SeqIO.parse(fastafile, "fasta"):
        records.append(record)

    for x in records:
        for y in records:
            score = pairwise2.align.globalxs(x.seq, y.seq, -1, -1, score_only=True)
            smaller_seq = len(x.seq) if len(x.seq) < len(y.seq) else len(y.seq)
            distances[(x.id, y.id)] = smaller_seq - score

    return distances

def calculate_distances(fastafile, fastqfile):
    distances = {}

    for x in SeqIO.parse(fastafile, "fasta"):
        scores = {}
        fastqfile.seek(0)
        for y in SeqIO.parse(fastqfile, "fastq"):
            score = pairwise2.align.globalxs(x.seq, y.seq, -1, -1, penalize_end_gaps=False, score_only=True)
            smaller_seq = len(x.seq) if len(x.seq) < len(y.seq) else len(y.seq)
            score = smaller_seq - score

            if not scores.get(score):
                scores[score] = 0

            scores[score] += 1

        if not distances.get(x.id): 
            distances[x.id] = {}

        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        distances[x.id] = scores.copy()


    return distances


def handle_uploaded_file(f, file_name):
    with open(os.path.join(MEDIA_ROOT, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            handle_uploaded_file(request.FILES['file'], title)
            request.session['files'] = title
            return HttpResponseRedirect('results')
    else:
        form = UploadFileForm()
    return render(request, 'preprocess/upload.html', {'form': form})
