from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import datetime, os
from django.http import JsonResponse
from operator import itemgetter
from time import sleep

def subdirs(path):
    for d in filter(os.path.isdir, os.listdir(path)):
        yield d
        
def files(path):
    for f in filter(os.path.isfile, os.listdir(path)):
        yield f

def test(request):
    return HttpResponse("Testing...")

def dt(request):
    now = datetime.datetime.now()
    html = "<html><body>%s</body></html>" % now
    return HttpResponse(html)

def none(request):
    html = "<html><body>Sorry, nothing found for that URL</body></html>"
    return HttpResponseNotFound(html)

def index(request):
    return render(request, 'index.html', {'name': settings.PROJECT_NAME })

def env(request):
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
                }
    
    for key, value in os.environ.items():
        ret_dict['data'].append((key[:30], value[:80]))
        ret_dict['recordsTotal'] += 1
    
    ret_dict['data'] = sorted(ret_dict['data'])
    
    return JsonResponse(ret_dict)

def proc(request):
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
                }
    
    processoutput = os.popen("ps -Af").read()
    for proc in processoutput.split('\n')[1:]:
        output = proc.split()
        if output:
            name = output[7].split('/')[-1]
            if ']' in name:
                continue
            line = (name[:30], output[0], output[1], output[2], " ".join(output[8:]))
            ret_dict['data'].append(line)
            ret_dict['recordsTotal'] += 1
    
    ret_dict['data'] = sorted(ret_dict['data'],key=itemgetter(1))
    
    return JsonResponse(ret_dict)

def file(request):
    p = '.'
    html = '<ul>'
    for d in subdirs(p):
        html = html + "<li>%s</li>"%(d)
        for f in files(p+'/'+d):
            html = html + "<li>%s</li>"%(f)
            
    for f in files(p+'/'+d):
        html = html + "<li>%s</li>"%(f)
                    
    html = html + '</ul>'

    return HttpResponse(html)

def action(request):
    msg = "Failed"
    out = ' '
    if request.method == 'GET':
        if 'action' in request.GET and 'seconds' in request.GET:
            msg = "Simulating '%s' for '%s' seconds"%(request.GET['action'], request.GET['seconds'])
            if request.GET['action'] == 'hang':
                out = out + os.popen("kill -s STOP 1").read()
                print (out)
                sleep(int(request.GET['seconds']))
                out = out + os.popen("kill -s CONT 1").read()
                print (out)
            elif request.GET['action'] == 'kill':
                out = out + os.popen("kill 1").read()
                print (out)
            elif request.GET['action'] == 'fileio':
                pass
                
    return HttpResponse(msg+"\n"+out)



