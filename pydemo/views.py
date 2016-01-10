import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import datetime
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html', {'name': settings.PROJECT_NAME })

def test(request):
    return HttpResponse("Testing...")

def env(request):
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
                }
    
    for key, value in os.environ.items():
        ret_dict['data'].append((key, value))
        ret_dict['recordsTotal'] += 1
        
    return JsonResponse(ret_dict)

def dt(request):
    now = datetime.datetime.now()
    html = "<html><body>%s</body></html>" % now
    return HttpResponse(html)