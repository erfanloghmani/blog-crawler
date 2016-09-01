from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Blog, Link
from rest_framework import viewsets
from .serializers import BlogSerializer, LinkSerializer
import json

class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Blog.objects.all().order_by('id')
    serializer_class = BlogSerializer

class LinkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Link.objects.all().order_by('id')
    serializer_class = LinkSerializer

def index(request):
    context = {
        'blogs_length': len(Blog.objects.all()),
        'links_length': len(Link.objects.all()),
        'blog_page_count': (len(Blog.objects.all()) - 1) // 20 + 1,
    }
    return render(request, 'crawl/index.html', context)

def in_degrees(request, page):
    sorted_in_degrees = Paginator(sorted(Blog.objects.all(), key=lambda a: a.in_degree(), reverse=True), 20)
    p = sorted_in_degrees.page(page).object_list
    p = list(map(lambda a: a.id, p))
    return HttpResponse(json.dumps(p))

def out_degrees(request, page):
    sorted_out_degrees = Paginator(sorted(Blog.objects.all(), key=lambda a: a.out_degree(), reverse=True), 20)
    p = sorted_out_degrees.page(page).object_list
    p = list(map(lambda a: a.id, p))
    return HttpResponse(json.dumps(p))

def link_count(request):
    counts = []
    for blog in Blog.objects.all():
        counts.append((len(Link.objects.filter(dest=blog)), blog.name))
    counts.sort()
    return HttpResponse(str(counts))
