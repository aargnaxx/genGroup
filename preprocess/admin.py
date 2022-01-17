from django.contrib import admin

from .models import DistancesAnalysis, DistancesBetweenResultsAnalysis, SequenceLengthAnalysis

# Register your models here.

admin.site.register(DistancesAnalysis)
admin.site.register(DistancesBetweenResultsAnalysis)
admin.site.register(SequenceLengthAnalysis)
