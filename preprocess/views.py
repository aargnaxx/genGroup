import os

from Bio import SeqIO, pairwise2
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from genGroup.settings import MEDIA_ROOT

from .forms import SelectFileForm, SelectSequenceLength, UploadFileForm


class Preprocessing(APIView):
    def post(self, request, *args, **kwargs):
        file_to_analyze = request.POST.get('file_to_analyze')
        if file_to_analyze == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
                
        result_file = request.POST.get('result_file')
        if result_file == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(os.path.join(MEDIA_ROOT, "files/" + file_to_analyze)) as fastqfile:
                with open(os.path.join(MEDIA_ROOT, "files/" + result_file)) as fastafile:
                    sequence_lengths= calculate_sequence_lengths(fastqfile)
                    distances_between_results = calculate_distances_between_results(fastafile)

                    fastqfile.seek(0)
                    fastafile.seek(0)
                    distances = calculate_distances(fastafile, fastqfile)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = {'sequence_lengths': sequence_lengths, 'distances_between_results': distances_between_results, 'distances': distances}
        return Response(context, status=status.HTTP_200_OK)
        

def calculate_sequence_lengths(fastqfile):
    counts = {}
    for record in SeqIO.parse(fastqfile, "fastq"):
        seq_len = len(record.seq)

        if not counts.get(seq_len):
            counts[seq_len] = 0

        counts[seq_len] += 1

    return counts

def calculate_distances_between_results(fastafile):
    distances = []
    records = []
    for record in SeqIO.parse(fastafile, "fasta"):
        records.append(record)

    for x in records:
        for y in records:
            score = pairwise2.align.globalxs(x.seq, y.seq, -1, -1, score_only=True)
            smaller_seq = len(x.seq) if len(x.seq) < len(y.seq) else len(y.seq)
            smaller_seq = smaller_seq - score
            distances.append((x.id, y.id, smaller_seq))

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
