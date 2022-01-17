import json

from django.db import models

from files.models import AnalysisFile, ResultFile

# Create your models here.


class SequenceLengthAnalysis(models.Model):
    file = models.OneToOneField(AnalysisFile, on_delete=models.CASCADE)
    sequence_lengths = models.JSONField(null=True)

class DistancesBetweenResultsAnalysis(models.Model):
    file = models.OneToOneField(ResultFile, on_delete=models.CASCADE)
    distances = models.JSONField(null=True)

class DistancesAnalysis(models.Model):
    analysis_file = models.ForeignKey(AnalysisFile, on_delete=models.CASCADE)
    result_file = models.ForeignKey(ResultFile, on_delete=models.CASCADE)
    distances = models.JSONField(null=True)
