from collections import Counter
from threading import Thread

from Bio import SeqIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from files.models import AnalysisFile
from preprocess.scoring import Scoring
# from results.export_results import write_clustering_report_fasta

from .clustering import Clustering
from .models import ClusteringAnalysis, ScoringAnalysis


# Create your views here.

class ClusteringList(APIView):
    def post(self, request, *args, **kwargs):
        input_file = request.POST.get('input_file')
        if input_file is None:
            return Response("input_file parameter is missing ", status=status.HTTP_400_BAD_REQUEST)

        analysis_file, created = AnalysisFile.objects.get_or_create(name=input_file)

        sequence_length = request.POST.get('reading_length')
        if sequence_length is None:
            return Response("reading_length parameter is missing", status=status.HTTP_400_BAD_REQUEST)

        sequence_length = int(sequence_length)

        clustering_type = request.POST.get('clustering_type')
        if clustering_type is None:
            return Response("clustering_type parameter is missing", status=status.HTTP_400_BAD_REQUEST)

        num_clusters = request.POST.get('num_clusters')
        if num_clusters is None:
            return Response("num_clusters parameter is missing", status=status.HTTP_400_BAD_REQUEST)

        num_clusters = int(num_clusters)

        ca = ClusteringAnalysis.objects.filter(analysis_file=analysis_file, sequence_length=sequence_length,
                                               clustering_type=clustering_type, num_clusters=num_clusters)

        if not ca.count():
            ca = ClusteringAnalysis.objects.create(analysis_file=analysis_file, sequence_length=sequence_length,
                                                   clustering_type=clustering_type, num_clusters=num_clusters, status='IP')
        else:
            ca = ca.first()

        if not ca.results:
            t = Thread(target=run_clustering, args=(analysis_file, sequence_length, clustering_type, num_clusters, ca))
            t.start()
            return Response(ca.pk, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(ca.pk, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        cas = ClusteringAnalysis.objects.all()
        clustering_results = []
        for ca in cas:
            if not ca.results:
                continue
                
            ca_result = {
                "analysis_file": ca.analysis_file.name,
                "sequence_length": ca.sequence_length,
                "clustering_type": ca.clustering_type,
                "num_clusters": ca.num_clusters,
                "results": ca.results
            }
            clustering_results.append(ca_result)

        return Response(clustering_results, status=status.HTTP_200_OK)


class ClusteringView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            ca = ClusteringAnalysis.objects.get(pk=pk)
            if ca.results:
                return Response(ca.results, status=status.HTTP_200_OK)

            return Response("Results not yet available", status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ClusteringStatus(APIView):
    def get(self, request, *args, **kwargs):
        cas = ClusteringAnalysis.objects.all()
        statuses = []
        for ca in cas:
            s = {
                "id": ca.pk,
                "status": ca.status,
                "analysis_file": ca.analysis_file.name,
                "sequence_length": ca.sequence_length,
                "clustering_type": ca.clustering_type,
                "num_clusters": ca.num_clusters,
                "results": ca.results
            }

            statuses.append(s)
        return Response(statuses, status=status.HTTP_200_OK)


def run_clustering(analysis_file, sequence_length, clustering_type, num_clusters, ca):
    try:
        sa = ScoringAnalysis.objects.filter(analysis_file=analysis_file, sequence_length=sequence_length)
        if not sa.count():
            sa = ScoringAnalysis.objects.create(analysis_file=analysis_file, sequence_length=sequence_length)
        else:
            sa = sa.first()

        if not sa.scores:
            sc = Scoring(analysis_file.name, sequence_length)
            sc.score_calc()
            sa.scores = sc.score
            sa.save()

        cl = Clustering(scores=sa.scores, reading_length=sequence_length, clustering_type=clustering_type,
                        num_clusters=num_clusters)
        c = Counter(cl.results.labels_)
        results = {}
        for key in c.keys():
            results[str(key)] = c[key]

        results["centers"] = cl.centers

        ca.results = results
        # write_clustering_report_fasta(
        #     f'report_{clustering_type}_{sequence_length}_{num_clusters}.fasta', [sc.sequences[i] for i in cl.centers])
        ca.status = 'SU'
        ca.save()
    except:
        ca.status = 'FA'
        ca.save()


def filter_out(fastqfile, seq_range):
    filtered_records = []
    for record in SeqIO.parse(fastqfile, "fastq"):
        if len(record.seq) in seq_range:
            filtered_records.append(record.seq)

    return filtered_records
