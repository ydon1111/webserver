from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CSVData
import csv

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # CSV 파일 저장
            csv_data = form.save()
            # CSV 파일 처리 로직을 여기에 추가
            # 예: csv_data.csv_file.path를 사용하여 파일 경로 가져오기

            # CSV 파일 처리가 끝나면 리디렉션 또는 다른 작업을 수행
            return redirect('success')
    else:
        form = CSVUploadForm()
    return render(request, 'demo/csv_upload.html', {'form': form})

def success(request):
    return render(request, 'demo/success.html')