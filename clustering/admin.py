from django.contrib import admin

from .models import ClusteringAnalysis, ScoringAnalysis

# Register your models here.

admin.site.register(ClusteringAnalysis)
admin.site.register(ScoringAnalysis)
