# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('crawl_status', models.CharField(max_length=1, choices=[(b'N', b'Not Yet'), (b'Y', b'Done')])),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dest', models.ForeignKey(related_name='dest', to='crawl.Blog')),
                ('src', models.ForeignKey(related_name='src', to='crawl.Blog')),
            ],
        ),
    ]
