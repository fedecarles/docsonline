# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-28 02:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0014_auto_20160628_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='a492bd9c-1', max_length=120, unique=True),
        ),
    ]