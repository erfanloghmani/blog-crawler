from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog, Link
from collections import deque
import json

class Command(BaseCommand):
    help = 'create json from db'

    def add_arguments(self, parser):
        parser.add_argument(
            '--blog',
            dest='blog',
            default='',
            help='which blog to create json',
        )

    def handle(self, *args, **options):
        if options['blog'] == '':
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
        else:
            output = {}
            b = Blog.objects.filter(name=options['blog'])[0]
            d = deque()
            nodes = {}
            d.append(b)
            nodes[b.id] = {'id': b.id, 'name': b.name, 'dist': 0}
            links = []
            while len(d) > 0:
                x = d.pop()
                if nodes[x.id]['dist'] < 2:
                    for src in x.src.all():
                        links.append({'source': x.id, 'target': src.dest.id})
                        try:
                            nodes[src.dest.id]
                        except:
                            nodes[src.dest.id] = {'id': src.dest.id, 'name': src.dest.name,
                                                  'dist': nodes[x.id]['dist'] + 1}
                            d.append(src.dest)
                for dest in x.dest.all():
                    links.append({'source': dest.src.id, 'target': x.id})
                    try:
                        nodes[dest.src.id]
                    except:
                        nodes[dest.src.id] = {'id': dest.src.id, 'name': dest.src.name, 'dist': nodes[x.id]['dist'] + 1}
                        d.append(dest.src)

            nodes_list = []
            for key, value in nodes.items():
                nodes_list.append(value)

            output['nodes'] = nodes_list
            output['links'] = links
            self.stdout.write(json.dumps(output))