# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-26 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0003_auto_20160626_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='0d10b77d-e', max_length=120, unique=True),
        ),
    ]
