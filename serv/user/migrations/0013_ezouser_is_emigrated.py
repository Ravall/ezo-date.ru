# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_ezouser_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='ezouser',
            name='is_emigrated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
