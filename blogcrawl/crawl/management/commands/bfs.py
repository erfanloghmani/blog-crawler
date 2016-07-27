from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog
from collections import deque

class Command(BaseCommand):
    help = 'bfs on blog network'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs=1, type=int)

    def handle(self, *args, **options):
        count = options['count'][0]
        d = deque()
        for blog in Blog.objects.filter(crawl_status='N'):
            d.append(blog)
        c = 0
        while d and c < count:
            blog = d.popleft()
            for nblog in blog.crawl():
                d.append(nblog)
            c += 1