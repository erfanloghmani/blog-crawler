# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-03 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0006_auto_20160902_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='coeffition',
            field=models.FloatField(default=0, null=True),
        ),
    ]