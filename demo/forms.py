from django import forms
from demo.models import CSVData

# class CSVUploadForm(forms.ModelForm):
#     class Meta:
#         model = CSVData
#         fields = ["csv_info"]


class UploadForm(forms.Form):
    csv_file = forms.FileField()