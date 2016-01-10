import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

def index(request):
    return render(request, 'index.html', {'name': settings.PROJECT_NAME })

def test(request):
    return HttpResponse("Testing...")

def procs(request):
    return render(request, 'procs.html', {'key': 'value'})
