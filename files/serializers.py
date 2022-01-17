from rest_framework import serializers
from .models import AnalysisFile

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisFile
        fields = '__all__'
