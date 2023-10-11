from django.shortcuts import render
from django.views.generic.base import View

import csv 
from io import TextIOWrapper

from django.db import connection

from .forms import UploadForm
from demo.models import CSVData



def upload_csv(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_data = CSVData(csv_file=request.FILES['csv_file'])
            csv_data.save()
            return render(request, 'demo/success.html')
    else:
        form = UploadForm()
    return render(request, 'demo/upload.html', {'form': form})












# 데이터베이스 작업 수행
connection.close()  # 연결을 닫음