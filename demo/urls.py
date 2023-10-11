from django.urls import path
from demo.views import UploadView


app_name = 'demo'

urlpatterns = [
    path('upload/', UploadView.as_view(),name='uploade_view'),
]