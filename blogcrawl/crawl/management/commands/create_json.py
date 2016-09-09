from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog, Link
from collections import deque
import json

class Command(BaseCommand):
    help = 'create json from db'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            dest='type',
            default='',
            help='which type of links to have',
        )


    def handle(self, *args, **options):
        graph = {}
        if options['type'] == 'out':
            for blog in Blog.objects.all():
                graph[blog.id] = []
                for src in blog.src.all():
                    graph[blog.id].append(str(src.dest.id))

        elif options['type'] == 'in':
            for blog in Blog.objects.all():
                graph[blog.id] = []
                for dest in blog.dest.all():
                    graph[blog.id].append(str(dest.src.id))
        else:
            for blog in Blog.objects.all():
                graph[blog.id] = []
                for src in blog.src.all():
                    graph[blog.id].append(str(src.dest.id))
                for dest in blog.dest.all():
                    if str(dest.src.id) not in graph[blog.id]:
                        graph[blog.id].append(str(dest.src.id))
        self.stdout.write(json.dumps(graph))