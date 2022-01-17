from django.contrib import admin
from .models import AnalysisFile, ResultFile

# Register your models here.

admin.site.register(AnalysisFile)
admin.site.register(ResultFile)
