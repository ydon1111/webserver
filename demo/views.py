from django.shortcuts import render
from django.views.generic.base import View

from .forms import UploadForm



class UploadView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "demo/upload.html", {"form": UploadForm()})