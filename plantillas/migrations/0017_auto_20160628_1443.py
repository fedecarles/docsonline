# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-28 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0016_auto_20160628_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='c17b65a9-1', max_length=120, unique=True),
        ),
    ]