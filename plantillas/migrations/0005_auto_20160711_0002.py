# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-11 00:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0004_auto_20160710_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='place',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='plantillamodel',
            name='creation_date',
            field=models.CharField(default='11-07-2016', max_length=30),
        ),
        migrations.AlterField(
            model_name='plantillamodel',
            name='doc_id',
            field=models.CharField(default='bebdec6e-8', max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
