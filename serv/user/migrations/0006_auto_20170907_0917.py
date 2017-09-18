# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_ezouser_date_born'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ezouser',
            old_name='city_born',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='ezouser',
            name='city_live',
        ),
    ]
