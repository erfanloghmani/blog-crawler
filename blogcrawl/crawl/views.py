from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json
from .models import Blog, Link
# Create your views here.

def index(request):
    blog_count = len(Blog.objects.all())
    link_count = len(Link.objects.all())
    return HttpResponse('#blog: ' + str(blog_count) + ' #link: ' + str(link_count))

def json_export(request):
    output = {}
    nodes = []
    for blog in Blog.objects.all():
        nodes.append({'id': blog.pk, 'name': blog.name})
    links = []
    for link in Link.objects.all():
        links.append({'src': link.src.pk, 'dest': link.dest.pk})

    output['nodes'] = nodes
    output['links'] = links

    return HttpResponse(json.dumps(output))

