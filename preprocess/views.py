import os

from Bio import SeqIO, pairwise2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from genGroup.settings import MEDIA_ROOT

from files.models import AnalysisFile, ResultFile
from preprocess.models import SequenceLengthAnalysis, DistancesAnalysis, DistancesBetweenResultsAnalysis


class Preprocessing(APIView):
    def post(self, request, *args, **kwargs):
        file_to_analyze = request.POST.get('file_to_analyze')
        if file_to_analyze == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file_to_analyze, created = AnalysisFile.objects.get_or_create(name=file_to_analyze)
                
        result_file = request.POST.get('result_file')
        if result_file == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        result_file, created = ResultFile.objects.get_or_create(name=result_file)

        try:
            if not hasattr(file_to_analyze, "sequencelengthanalysis"):
                with open(os.path.join(MEDIA_ROOT, "files/" + file_to_analyze.name)) as fastqfile:
                    sequence_lengths= calculate_sequence_lengths(fastqfile)
                    SequenceLengthAnalysis.objects.create(file=file_to_analyze, sequence_lengths=sequence_lengths)


            if not hasattr(result_file, "distancesbetweenresultsanalysis"):
                with open(os.path.join(MEDIA_ROOT, "files/" + result_file.name)) as fastafile:
                    distances_between_results = calculate_distances_between_results(fastafile)
                    DistancesBetweenResultsAnalysis.objects.create(file=result_file, distances=distances_between_results)

            if not file_to_analyze.distancesanalysis_set.filter(result_file=result_file).count():
                with open(os.path.join(MEDIA_ROOT, "files/" + file_to_analyze.name)) as fastqfile:
                    with open(os.path.join(MEDIA_ROOT, "files/" + result_file.name)) as fastafile:
                        distances = calculate_distances(fastafile, fastqfile)
                        DistancesAnalysis.objects.create(analysis_file=file_to_analyze, result_file=result_file, distances=distances)
        except Exception as e:
            return Response(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            sequence_lengths = file_to_analyze.sequencelengthanalysis.sequence_lengths
            distances_between_results = result_file.distancesbetweenresultsanalysis.distances
            distances= file_to_analyze.distancesanalysis_set.get(result_file=result_file).distances
        except Exception as e:
            return Response(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

            if score > 35:
                continue

            if not scores.get(score):
                scores[score] = 0

            scores[score] += 1

        aggregated_scores = [0] * 36
        for i in range(36):
            score = scores.get(i, 0)

            if i != 0:
                score = score + aggregated_scores[i-1]
            aggregated_scores[i] = score

        if not distances.get(x.id): 
            distances[x.id] = {}

        distances[x.id] = aggregated_scores.copy()

    return distances
