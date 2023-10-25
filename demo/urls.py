from django.urls import path
from .views import upload_views,calculate_views


app_name = 'demo'

urlpatterns = [
    #upload_views.py 
    path('upload/', upload_views.upload_csv, name='upload_csv'),
    path('result/', calculate_views.show_analysis_result, name='result'),
]