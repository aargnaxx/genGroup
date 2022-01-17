import os
from threading import Thread

from Bio import SeqIO
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from files.models import AnalysisFile
from genGroup.settings import MEDIA_ROOT
from preprocess.scoring import Scoring

from .clustering import Clustering
from .models import ClusteringAnalysis

# Create your views here.

class ClusteringList(APIView):
    def post(self, request, *args, **kwargs):
        input_file = request.POST.get('input_file')
        if input_file == None:
            return Response("input_file parameter is missing ",status=status.HTTP_400_BAD_REQUEST)

        analysis_file, created = AnalysisFile.objects.get_or_create(name=input_file)

        sequence_length = request.POST.get('reading_length')
        if sequence_length == None:
            return Response("reading_length parameter is missing", status=status.HTTP_400_BAD_REQUEST)

        clustering_type = request.POST.get('clustering_type')
        if clustering_type == None:
            return Response("clustering_type parameter is missing", status=status.HTTP_400_BAD_REQUEST)

        num_clusters = request.POST.get('num_clusters')
        if num_clusters == None:
            return Response("num_clusters parameter is missing", status=status.HTTP_400_BAD_REQUEST)

        ca = ClusteringAnalysis.objects.filter(analysis_file=analysis_file, sequence_length=sequence_length, clustering_type=clustering_type, num_clusters=num_clusters)
        
        if not ca.count():
            ca = ClusteringAnalysis.objects.create(analysis_file=analysis_file, sequence_length=sequence_length, clustering_type=clustering_type, num_clusters=num_clusters)
            t = Thread(target=run_clustering, args=(analysis_file, sequence_length, clustering_type, num_clusters, ca))
            return Response(ca.pk, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(ca.first().pk, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        ca = ClusteringAnalysis.objects.all()
        return Response(ca, status=status.HTTP_200_OK)

class ClusteringView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            ca = ClusteringAnalysis.objects.get(pk=pk)
            return Response(ca.results, status=status.HTTP_200_ok)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

def run_clustering(analysis_file, sequence_length, clustering_type, num_clusters, ca):
    sc = Scoring(analysis_file, sequence_length)
    sc.score_calc()
    cl = Clustering(scores=sc.score, reading_length=sequence_length, clustering_type=clustering_type, num_clusters=num_clusters)

    ca = ClusteringAnalysis.objects.create(analysis_file=analysis_file, sequence_length=sequence_length, clustering_type=clustering_type, num_clusters=num_clusters, results=ca.results.labels_)

def filter_out(fastqfile, seq_range):
    filtered_records = []
    for record in SeqIO.parse(fastqfile, "fastq"):
        if len(record.seq) in seq_range:
            filtered_records.append(record.seq)

    return filtered_records
