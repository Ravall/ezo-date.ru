# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SxgeoCities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region_id', models.IntegerField()),
                ('name_ru', models.CharField(max_length=128, db_index=True)),
                ('name_en', models.CharField(max_length=128)),
                ('lat', models.DecimalField(max_digits=10, decimal_places=5)),
                ('lon', models.DecimalField(max_digits=10, decimal_places=5)),
                ('okato', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'sxgeo_cities',
            },
        ),
        migrations.CreateModel(
            name='SxgeoCountry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso', models.CharField(max_length=2)),
                ('continent', models.CharField(max_length=2)),
                ('name_ru', models.CharField(max_length=128)),
                ('name_en', models.CharField(max_length=128)),
                ('lat', models.DecimalField(max_digits=6, decimal_places=2)),
                ('lon', models.DecimalField(max_digits=6, decimal_places=2)),
                ('timezone', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'sxgeo_country',
            },
        ),
        migrations.CreateModel(
            name='SxgeoRegions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso', models.CharField(max_length=7)),
                ('country', models.CharField(max_length=2, db_index=True)),
                ('name_ru', models.CharField(max_length=128)),
                ('name_en', models.CharField(max_length=128)),
                ('timezone', models.CharField(max_length=30)),
                ('okato', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'sxgeo_regions',
            },
        ),
    ]
