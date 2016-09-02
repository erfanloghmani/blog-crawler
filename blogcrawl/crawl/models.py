from django.db import models
from django.db import IntegrityError
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

    def find_post(self):
        while True:
            try:
                r = requests.get('http://' + self.name + '.blog.ir/')
            except:
                continue
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            posts = soup.find_all(class_='post')
            post = posts[0]
            title = post.find_all(class_=re.compile('title'))[0].find_all('a')[0]
        except:
            title_classes = ['title', 'title align', 'PostTitle']
            for title_class in title_classes:
                for t in soup.find_all(class_=title_class):
                    if len(t.find_all('a')) > 0:
                        title = t.find_all('a')[0]
                        break
            try:
                title
            except:
                tags = ['h2']
                for tag in tags:
                    for t in soup.find_all(tag):
                        if len(t.find_all('a')) > 0:
                            title = t.find_all('a')[0]
                            break


        try:
            post = Post()
            post.blog = self
            post.title = title.string
            post.url = 'http://' + self.name + '.blog.ir' + title['href']
            post.save()
        except IntegrityError:
            pass

    def in_degree_count(self):
        return len(self.dest.all())

    def out_degree_count(self):
        return len(self.src.all())


class Post(models.Model):
    blog = models.ForeignKey(Blog, related_name="post")
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=400, unique=True)

    def get_text(self):
        while True:
            try:
                r = requests.get(self.url)
            except:
                continue
            break
        soup = BeautifulSoup(r.text, 'html.parser')
        body_classes = ['body', 'post-content', 'context', 'PostContent']
        for body_class in body_classes:
            if len(soup.find_all(class_=body_class)) > 0:
                body = soup.find_all(class_=body_class)[0].descendants
                break

        try:
            body
        except:
            body = ['empty']
        return body

class Link(models.Model):
    src = models.ForeignKey(Blog, related_name="src")
    dest = models.ForeignKey(Blog, related_name="dest")
