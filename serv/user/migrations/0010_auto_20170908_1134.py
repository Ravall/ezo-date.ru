# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20170907_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ezouser',
            name='date',
        ),
        migrations.RemoveField(
            model_name='ezouser',
            name='time',
        ),
        migrations.AddField(
            model_name='ezouser',
            name='born_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
