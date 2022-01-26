from django.db import models

from preprocess.models import *
from files.models import *

# Create your models here.


class ClusteringAnalysis(models.Model):
    STATUS_CHOICES = [
        ('IP', 'IN_PROGRESS'),
        ('FA', 'FAILED'),
        ('SU', 'SUCCEEDED'),
        ('UN', 'UNKNOWN'),
    ]
    
    analysis_file = models.ForeignKey(AnalysisFile, on_delete=models.CASCADE)
    sequence_length = models.PositiveIntegerField()
    clustering_type = models.CharField(max_length=50)
    num_clusters = models.PositiveIntegerField()
    results = models.JSONField(null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='UN')


class ScoringAnalysis(models.Model):
    analysis_file = models.ForeignKey(AnalysisFile, on_delete=models.CASCADE)
    sequence_length = models.PositiveIntegerField()
    scores = models.JSONField(null=True)
    sequences = models.JSONField(null=True)
