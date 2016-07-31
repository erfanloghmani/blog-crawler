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
            nodes.append({'id': blog.pk, 'name': blog.name})
        links = []
        for link in Link.objects.all():
            links.append({'src': link.src.pk, 'dest': link.dest.pk})

        output['nodes'] = nodes
        output['links'] = links
        self.stdout.write(json.dumps(output))