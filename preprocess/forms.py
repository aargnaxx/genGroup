from django import forms
from django.conf import settings


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SelectFileForm(forms.Form):
    files = forms.FilePathField(path=settings.MEDIA_ROOT, match=".fastq")
