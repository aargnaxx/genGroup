from django.db import models

from preprocess.models import *
from files.models import *

# Create your models here.


class Analysis(models.Model):
    analysis_file = models.CharField(max_length=256)
    result_file = models.CharField(max_length=256, default='')
    seq_length = models.IntegerField()
    decrement_range = models.IntegerField()
    increment_range = models.IntegerField()


class ClusteringAnalysis(models.Model):
    analysis_file = models.ForeignKey(AnalysisFile, on_delete=models.CASCADE)
    sequence_length = models.PositiveIntegerField()
    clustering_type = models.CharField(max_length=50)
    num_clusters = models.PositiveIntegerField()
    results = models.JSONField(null=True)


class ScoringAnalysis(models.Model):
    analysis_file = models.ForeignKey(AnalysisFile, on_delete=models.CASCADE)
    sequence_length = models.PositiveIntegerField()
    scores = models.JSONField(null=True)