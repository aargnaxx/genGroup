import os

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from Bio import SeqIO

from genGroup.settings import MEDIA_ROOT

from .forms import SelectFileForm, SelectSequenceLength, UploadFileForm


# Shows up when user goes to '/preprocess/'.
def select_file(request):
    if request.method == 'POST':
        form = SelectFileForm(request.POST)
        if form.is_valid():
            request.session['files'] = request.POST['files']
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

            return redirect('clustering:run', seq_length=chosen_seq_length)

    file = request.session.get('files')
    with open(os.path.join(MEDIA_ROOT, file)) as f:
        sequence_data = preprocess(f)

    sequence_data = dict(
        sorted(sequence_data.items(), key=lambda item: item[1], reverse=True))

    sorted_sequence_lengths = sorted(sequence_data.keys(), reverse=True)
    request.session['sequence_lengths'] = sorted_sequence_lengths

    form = SelectSequenceLength(sorted_sequence_lengths)

    context = {'form': form, 'result': sequence_data}
    return render(request, 'preprocess/preprocess_results.html', context)


def preprocess(fastqfile):
    counts = {}
    for record in SeqIO.parse(fastqfile, "fastq"):
        seq_len = len(record.seq)

        if not counts.get(seq_len):
            counts[seq_len] = 0

        counts[seq_len] += 1

    return counts


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
