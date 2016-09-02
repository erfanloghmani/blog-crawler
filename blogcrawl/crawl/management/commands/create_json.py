from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog, Link
import json

class Command(BaseCommand):
    help = 'create json from db'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        output = {}
        nodes = []
        for blog in Blog.objects.all():
            if len(blog.src.all()) > 0 or len(blog.dest.all()) > 0:
                nodes.append({'id': blog.pk, 'name': blog.name})
        links = []
        for link in Link.objects.all():
            links.append({'source': link.src.pk, 'target': link.dest.pk})

        output['nodes'] = nodes
        output['links'] = links
        self.stdout.write(json.dumps(output))