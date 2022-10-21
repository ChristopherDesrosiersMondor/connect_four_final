import json
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# https://www.javatpoint.com/django-session

def home(request):
    return render(
        request,
        'connect_four/base.html'
    )

def request_access(request):
    a = request.POST.get('request_data')
    request.session['id'] = a.toString()
    return HttpResponse("session is set")

def print_id(request):
    id = request.session['id']
    return render(
    request,
    'connect_four/base.html',
    {
        'id': id
    }
    )