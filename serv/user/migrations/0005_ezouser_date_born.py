# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_ezouser_date_born'),
    ]

    operations = [
        migrations.AddField(
            model_name='ezouser',
            name='date_born',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
