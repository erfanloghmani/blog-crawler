from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog

class Command(BaseCommand):
    help = 'Creates new blog'

    def add_arguments(self, parser):
        parser.add_argument('blog_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for blog_name in options['blog_name']:
            blog = Blog()
            blog.name = blog_name
            blog.crawl_status = 'N'
            blog.save()