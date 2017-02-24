# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0011_auto_20170216_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.AlterField(
            model_name='plantillamodel',
            name='creation_date',
            field=models.CharField(default='18-02-2017', max_length=30),
        ),
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='9153d094-b', max_length=120, unique=True),
        ),
    ]