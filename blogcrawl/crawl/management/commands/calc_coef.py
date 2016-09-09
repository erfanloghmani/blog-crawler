from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from crawl.models import Blog
import json

class Command(BaseCommand):
    help = 'calculate coeffions with json graph'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('/tmp/command_output', 'w') as f:
            call_command('create_json', type='all', stdout=f)
        with open('/tmp/command_output', 'r') as f:
            strData = f.read()
            graph = json.loads(strData)
        k = 0
        for key, neighbours in graph.items():
            if k % 100 == 0:
                self.stdout.write(str(k) + ' passed')
            k += 1
            count = 0
            addj = {}
            for neighbour in neighbours:
                addj[neighbour] = True
            for neighbour in neighbours:
                for nn in graph[neighbour]:
                    if nn in addj:
                        count += 1

            b = Blog.objects.get(id=key)
            try:
                b.coeffition = count / (len(neighbours) ** 2)
            except ZeroDivisionError:
                b.coeffition = 0
            b.save()