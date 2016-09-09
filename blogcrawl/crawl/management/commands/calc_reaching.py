from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from crawl.models import Blog
from collections import deque
import json

class Command(BaseCommand):
    help = 'calculate reaching blog count with json graph'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('/tmp/command_output', 'w') as f:
            call_command('create_json', type='in', stdout=f)
        with open('/tmp/command_output', 'r') as f:
            strData = f.read()
            graph = json.loads(strData)
        k = 0
        for key, neighbours in graph.items():
            if k % 100 == 0:
                self.stdout.write(str(k) + ' passed')
            k += 1
            source = key

            d = deque()
            seen = {}
            d.append(source)
            seen[source] = True
            while len(d) > 0:
                x = d.popleft()
                for n in graph[x]:
                    if n not in seen:
                        d.append(n)
                        seen[n] = True

            b = Blog.objects.get(id=key)
            b.reaching_count = len(seen)
            b.save()