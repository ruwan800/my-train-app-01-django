from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
import shutil
import os
import sys
from django.http.response import HttpResponse
from documentation.configuresphinxsource import configureSphinxSourceFile


def renderHTML(request,file):
    return render_to_response("doc/{}".format(file))
def renderCSS(request,file):
    return render_to_response("doc/{}".format(file),content_type='text/css')
def renderJS(request,file):
    return render_to_response("doc/{}".format(file),content_type='text/javascript')
def renderObj(request,file):
    html_path = os.path.join(os.path.dirname(__file__), "templates","doc")
    image_data = open(os.path.join(html_path, file), "rb").read()
    return HttpResponse(image_data, mimetype="image")

def index(request):
    return render_to_response('doc/index.html',{}, context_instance=RequestContext(request))

def generate(request):
    #return render_to_response('doc/index.html',{}, context_instance=RequestContext(request))####
    doc_path = os.path.dirname(__file__)
    gen_path = os.path.join(doc_path, "gen")
    html_path = os.path.join(doc_path, "templates","doc")
    build_path = os.path.join(gen_path, "_build","html")
    gen_file = os.path.join(gen_path, "gen.sh")
    configureSphinxSourceFile()
    shutil.rmtree(html_path)
    f = open(gen_file,'w')
    f.write("#auto generated file\n")
    f.write("export DJANGO_SETTINGS_MODULE={}\n".format(os.environ['DJANGO_SETTINGS_MODULE']))
    f.write("cd {}\n".format(gen_path))
    f.write("make html")
    f.close()
    msg = os.system("sh {}".format(gen_file))
    print(msg)
    shutil.copytree(build_path, html_path)
    return render_to_response('doc/index.html',{}, context_instance=RequestContext(request))

