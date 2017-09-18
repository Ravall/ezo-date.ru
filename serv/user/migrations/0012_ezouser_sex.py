# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20170912_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='ezouser',
            name='sex',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
    ]
