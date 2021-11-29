import os
from django.http.response import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.shortcuts import render

from Bio import SeqIO

from genGroup.settings import MEDIA_ROOT

from .forms import SelectFileForm, UploadFileForm


def index(request):
    return HttpResponse("Hello, world. You're at the preprocess index.")


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


class FileFieldFormView(FormView):
    form_class = UploadFileForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '/preprocess/list'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def list_files(request):
    #fastq_files = os.listdir(settings.MEDIA_ROOT)
    # context = {
    #    'files': fastq_files,
    # }

    if request.method == 'POST':
        form = SelectFileForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/choose/')
    else:
        form = SelectFileForm()

    return render(request, 'preprocess/default_view.html', {'form': form})


def preprocess_results(request):
    file = request.POST['files']
    with open(os.path.join(MEDIA_ROOT, file)) as f:
        result = preprocess(f)

    result = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True))
    context = {'result': result}
    return render(request, 'preprocess/preprocess_results.html', context)


def preprocess(fastqfile):
    counts = {}
    for record in SeqIO.parse(fastqfile, "fastq"):
        seq_len = len(record.seq)

        if not counts.get(seq_len):
            counts[seq_len] = 0

        counts[seq_len] += 1

    print(counts)
    return counts
