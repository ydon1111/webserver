from django import forms
from demo.models import CSVData



class UploadForm(forms.Form):
    ppi_file = forms.FileField()