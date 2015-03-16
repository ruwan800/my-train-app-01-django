from django.http.response import HttpResponse
import json
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def renderJSON(request, data):
    json_data = json.dumps(data)
    return HttpResponse(json_data, mimetype='application/json')

def renderForm(request, ref, form):
    return render_to_response('form.html',{'content':form, 'ref':ref }, context_instance=RequestContext(request))
