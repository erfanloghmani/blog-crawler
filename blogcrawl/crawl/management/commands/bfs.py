from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog
from collections import deque

def append_to_deque(d, blog):
    blog.crawl_status = 'Q'
    blog.save()
    d.append(blog)

class Command(BaseCommand):
    help = 'bfs on blog network'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs=1, type=int)

    def handle(self, *args, **options):
        count = options['count'][0]
        d = deque()
        try:
            for blog in Blog.objects.filter(crawl_status='N'):
                append_to_deque(d, blog)
            c = 0
            while d and c < count:
                blog = d.popleft()
                for nblog in blog.crawl():
                    append_to_deque(d, nblog)
                c += 1
        finally:
            # clean crawl_status for objects in queue
            while d:
                blog = d.popleft()
                blog.crawl_status = 'N'
                blog.save()