# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-28 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20160628_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]