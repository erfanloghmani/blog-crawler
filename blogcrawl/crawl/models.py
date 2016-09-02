from django.db import models
from bs4 import BeautifulSoup
import requests
import re
# Create your models here.
class Blog(models.Model):
    CRAWL_STATUS = (
        ('N', 'Not Yet'),
        ('Q', 'In Queue'),
        ('Y', 'Done'),
    )
    name = models.CharField(max_length=60, unique=True)
    crawl_status = models.CharField(max_length=1, choices=CRAWL_STATUS)
    in_degree = models.IntegerField(null=True, default=0)
    out_degree = models.IntegerField(null=True, default=0)

    def find_links(self):
        found_links = set()
        while True:
            try:
                r = requests.get('http://' + self.name + '.blog.ir/')
            except requests.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
            except:
                continue
            break

        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('a'):
            try:
                link = a['href']
                m = re.match(r'http://(?P<name>\w+)\.blog.ir/', link)
                if m:
                    found_links.add(m.group('name'))
            except KeyError:
                continue
        return(found_links)

    def crawl(self):
        not_crawled_blogs = []
        dest_names = self.find_links()
        for dest_name in dest_names:
            if not Blog.objects.filter(name=dest_name):
                dest = Blog()
                dest.name = dest_name
                dest.crawl_status = 'N'
                dest.save()
                not_crawled_blogs.append(dest)
            else:
                dest = Blog.objects.filter(name=dest_name)[0]
                if dest.crawl_status == 'N':
                    not_crawled_blogs.append(dest)
            if not Link.objects.filter(src=self, dest=dest):
                link = Link()
                link.src = self
                self.out_degree = self.out_degree + 1
                link.dest = dest
                dest.in_degree = dest.in_degree + 1
                self.save()
                dest.save()
                link.save()
        self.crawl_status = 'Y'
        print(self.name + ' crowled')
        self.save()
        return not_crawled_blogs

    def in_degree_count(self):
        return len(self.dest.all())

    def out_degree_count(self):
        return len(self.src.all())

class Link(models.Model):
    src = models.ForeignKey(Blog, related_name="src")
    dest = models.ForeignKey(Blog, related_name="dest")
