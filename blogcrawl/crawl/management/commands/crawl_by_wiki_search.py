from django.core.management.base import BaseCommand, CommandError
from crawl.models import Blog
from bs4 import BeautifulSoup
import requests
import re
import time

class Command(BaseCommand):
    help = 'crawl blogs by search word from wikipedia random page'

    def add_arguments(self, parser):
        parser.add_argument(
            '--wait',
            dest='wait',
            default=0,
            help='how many seconds to wait',
        )

    def handle(self, *args, **options):
        self.crawl_by_wiki_search()
        if options['wait'] != 0:
            try:
                while True:
                    time.sleep(float(options['wait']))
                    self.crawl_by_wiki_search()
            except KeyboardInterrupt:
                self.stderr.write(self.style.ERROR('terminated'))

    def crawl_by_wiki_search(self):
        while True:
            try:
                r = requests.get(
                    'https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%98%D9%87:%D8%B5%D9%81%D8%AD%D9%87%D9%94_%D8%AA%D8%B5%D8%A7%D8%AF%D9%81%DB%8C')
            except:
                continue
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find(id='firstHeading')
        self.crawl_word(title.string)

    def crawl_word_start(self, word, start=0):
        while True:
            try:
                r = requests.get('http://blogs.salam.ir/blog.ir?q=' + word + '&start=' + str(start))
            except:
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

    def crawl_word(self, word):
        for i in range(0, 10):
            self.stdout.write('search for: ' + word + ', page: ' + str(i))
            self.crawl_word_start(word, i * 10)