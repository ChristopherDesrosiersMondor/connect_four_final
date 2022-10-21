import json
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(
        request,
        'connect_four/base.html'
    )

def request_access(request):
    print("DJANGO VIEW")
    a = request.POST.get('request_data')
    print(a)
    return HttpResponse(json.dumps(a),content_type="application/json")