from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    return render_to_response('home.html',{}, context_instance=RequestContext(request))

def test(request):
    return render_to_response('test.html',{}, context_instance=RequestContext(request))
