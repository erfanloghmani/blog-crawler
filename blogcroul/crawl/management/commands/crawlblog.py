from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog

class Command(BaseCommand):
    help = 'crawl links of blog'

    def add_arguments(self, parser):
        parser.add_argument('blog_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for blog_name in options['blog_name']:
            blog = Blog.objects.filter(name=blog_name)[0]
            blog.crawl()