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
        return Response({'files': files}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
