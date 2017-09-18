# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20150429_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ezouser',
            old_name='data_born',
            new_name='date_born',
        ),
    ]
