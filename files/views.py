import os

from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from genGroup.settings import MEDIA_ROOT

from .models import File
from .serializers import FileSerializer

# Create your views here.

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        path = os.path.join(MEDIA_ROOT, 'files')
        files = os.listdir(path)
        return JsonResponse({'files': files})

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def handle_uploaded_file(f, file_name):
    with open(os.path.join(MEDIA_ROOT, file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload(request):
    if request.method == 'POST':
        #form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        ##    title = form.cleaned_data.get('title')
        #    handle_uploaded_file(request.FILES['file'], title)
        #    request.session['files'] = title
        #    return HttpResponseRedirect('results')
        pass
    else:
        #form = UploadFileForm()
        pass
    return render(request, 'preprocess/upload.html')
