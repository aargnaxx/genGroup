import os
from django.http.response import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.shortcuts import render

from Bio import SeqIO

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
            handle_uploaded_file(
                request.FILES['file'], form.cleaned_data.get('title'))
            request.session['files'] = form.cleaned_data.get('title')
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
