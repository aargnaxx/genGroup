from django.db import models

# Create your models here.

class AnalysisFile(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    file = models.FileField(upload_to="files/")

    def __str__(self):
        return self.name

class ResultFile(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    file = models.FileField(upload_to="files/")

    def __str__(self):
        return self.name
