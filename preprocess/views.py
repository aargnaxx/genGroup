import os

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from Bio import SeqIO, SeqRecord

from genGroup.settings import MEDIA_ROOT

from .forms import SelectFileForm, UploadFileForm


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
    return render(request, 'upload.html', {'form': form})


def list_files(request):
    if request.method == 'POST':
        form = SelectFileForm(request.POST)
        if form.is_valid():
            request.session['files'] = request.POST['files']
            return HttpResponseRedirect('results')
    else:
        form = SelectFileForm()

    return render(request, 'default_view.html', {'form': form})


def preprocess_results(request):
    file = request.session.get('files')
    with open(os.path.join(MEDIA_ROOT, file)) as f:
        result = preprocess(f)

    result = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True))
    context = {'result': result}
    return render(request, 'preprocess_results.html', context)


def preprocess(fastqfile):
    counts = {}
    for record in SeqIO.parse(fastqfile, "fastq"):
        seq_len = len(record.seq)

        if not counts.get(seq_len):
            counts[seq_len] = 0

        counts[seq_len] += 1

    return counts


def filter_out(fastqfile, seq_len):
    filtered_records = []
    for record in SeqIO.parse(fastqfile, "fastq"):
        if len(record.seq) == seq_len:
            filtered_records.append(record.seq)

    return filtered_records
