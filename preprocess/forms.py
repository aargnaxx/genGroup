from django import forms
from django.conf import settings


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SelectFileForm(forms.Form):
    files = forms.FilePathField(path=settings.MEDIA_ROOT, match=".fastq")


class SelectSequenceLength(forms.Form):
    sequence_length = forms.ChoiceField(required=False)

    def __init__(self, given_choices, *args, **kwargs):
        super(SelectSequenceLength, self).__init__(*args, **kwargs)
        self.fields['sequence_length'] = forms.ChoiceField(
            choices=[(k, str(k)) for k in given_choices], required=False)
