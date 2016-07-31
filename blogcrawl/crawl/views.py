from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog, Link
# Create your views here.

def index(request):
    blog_count = len(Blog.objects.all())
    link_count = len(Link.objects.all())
    return HttpResponse('#blog: ' + str(blog_count) + ' #link: ' + str(link_count))
