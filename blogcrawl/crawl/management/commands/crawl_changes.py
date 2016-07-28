from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog
from bs4 import BeautifulSoup
import requests
import re
import time

def crawl_blog_changes():
    while True:
        try:
            r = requests.get('http://blog.ir/changes')
        except requests.ConnectionError:
            continue
        break
    soup = BeautifulSoup(r.text, 'html.parser')
    post_divs = soup.find_all("div", class_='post')
    for post in post_divs:
        for a in post.find_all('a'):
            link = a['href']
            m = re.match(r'http://(?P<name>\w+)\.blog.ir/', link)
            if m and not Blog.objects.filter(name=m.group('name')):
                print("new blog found: " + m.group('name'))
                blog = Blog()
                blog.name = m.group('name')
                blog.crawl_status = 'N'
                blog.save()

class Command(BaseCommand):
    help = 'crawl recently changed blogs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--wait',
            dest='wait',
            default=0,
            help='how many seconds to wait',
        )

    def handle(self, *args, **options):
        crawl_blog_changes()
        if options['wait'] != 0:
            try:
                while True:
                    time.sleep(float(options['wait']))
                    crawl_blog_changes()
            except:
                self.stderr.write(self.style.ERROR('terminated'))