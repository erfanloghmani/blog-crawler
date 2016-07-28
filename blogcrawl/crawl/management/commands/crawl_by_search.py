from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog
from bs4 import BeautifulSoup
import requests
import re
import time

def crawl_word_start(word, start=0):
    while True:
        try:
            r = requests.get('http://blogs.salam.ir/blog.ir?q=' + word + '&start=' + str(start))
        except requests.ConnectionError:
            continue
        break
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        try:
            link = a['href']
            m = re.match(r'http://(?P<name>\w+)\.blog.ir/', link)
            if m and not Blog.objects.filter(name=m.group('name')):
                print("new blog found: " + m.group('name'))
                blog = Blog()
                blog.name = m.group('name')
                blog.crawl_status = 'N'
                blog.save()
        except KeyError:
            pass

def crawl_word(word):
    for i in range(0,9):
        print('page: ' + str(i))
        crawl_word_start(word, i * 10)

class Command(BaseCommand):
    help = 'crawl blogs by search word in blogs'

    def add_arguments(self, parser):
        parser.add_argument('word', nargs='+', type=str)

    def handle(self, *args, **options):
        for word in options['word']:
            crawl_word(word)