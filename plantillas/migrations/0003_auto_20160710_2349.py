# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-10 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0002_auto_20160710_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='5ce6c14c-d', max_length=120, unique=True),
        ),
    ]