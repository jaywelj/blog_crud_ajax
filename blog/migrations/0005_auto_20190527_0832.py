# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-27 00:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190527_0807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='is_verified',
            new_name='flag',
        ),
    ]
