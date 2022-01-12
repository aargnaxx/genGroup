from django.db import models

# Create your models here.


class Analysis(models.Model):
    analysis_file = models.CharField(max_length=256)
    result_file = models.CharField(max_length=256)
    seq_length = models.IntegerField()
    decrement_range = models.IntegerField()
    increment_range = models.IntegerField()
