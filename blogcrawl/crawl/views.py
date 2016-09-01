from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog, Link
from rest_framework import viewsets
from .serializers import BlogSerializer, LinkSerializer


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
    blog_count = len(Blog.objects.all())
    link_count = len(Link.objects.all())
    return HttpResponse('#blog: ' + str(blog_count) + ' #link: ' + str(link_count))

def link_count(request):
    counts = []
    for blog in Blog.objects.all():
        counts.append((len(Link.objects.filter(dest=blog)), blog.name))
    counts.sort()
    return HttpResponse(str(counts))
