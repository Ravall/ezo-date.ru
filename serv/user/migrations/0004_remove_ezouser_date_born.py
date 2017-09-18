# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20170903_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ezouser',
            name='date_born',
        ),
    ]
