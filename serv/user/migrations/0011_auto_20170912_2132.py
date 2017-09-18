# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20170908_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='ezouser',
            name='city_live',
            field=models.ForeignKey(related_name='city_live', blank=True, to='user.SxGeoCity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ezouser',
            name='new_last_name',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ezouser',
            name='city',
            field=models.ForeignKey(related_name='city', blank=True, to='user.SxGeoCity', null=True),
            preserve_default=True,
        ),
    ]
