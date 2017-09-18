# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20170907_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ezouser',
            old_name='date_born',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='ezouser',
            old_name='time_born',
            new_name='time',
        ),
    ]
