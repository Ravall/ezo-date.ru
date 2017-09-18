# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20170907_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='SxGeoCity',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('region_id', models.IntegerField()),
                ('name_ru', models.CharField(max_length=128)),
                ('name_en', models.CharField(max_length=128)),
                ('lat', models.DecimalField(max_digits=10, decimal_places=5)),
                ('lon', models.DecimalField(max_digits=10, decimal_places=5)),
                ('okato', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'sxgeo_cities',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='ezouser',
            name='city',
            field=models.ForeignKey(blank=True, to='user.SxGeoCity', null=True),
            preserve_default=True,
        ),
    ]
