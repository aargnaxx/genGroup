from django import forms
from django.conf import settings
from django.db.models import PositiveIntegerField


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SelectFileForm(forms.Form):
    file_for_analysis = forms.FilePathField(path=settings.MEDIA_ROOT, match=".fastq")
    result_file = forms.FilePathField(path=settings.MEDIA_ROOT, match=".fasta")


class SelectSequenceLength(forms.Form):
    sequence_length = forms.ChoiceField(required=True)
    inc_offset = forms.IntegerField(min_value=0, initial=0)
    dec_offset = forms.IntegerField(min_value=0, initial=0)

    def __init__(self, given_choices, *args, **kwargs):
        super(SelectSequenceLength, self).__init__(*args, **kwargs)
        self.fields['sequence_length'] = forms.ChoiceField(
            choices=[(k, str(k)) for k in given_choices], required=True)
