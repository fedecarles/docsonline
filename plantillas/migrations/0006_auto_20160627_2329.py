# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-27 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0005_auto_20160627_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='8415e073-9', max_length=120, unique=True),
        ),
    ]