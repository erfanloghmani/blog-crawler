from django.contrib import admin
from .models import Blog, Post, Link
# Register your models here.
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Link)