# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class SxgeoCities(models.Model):
    region_id = models.IntegerField()
    name_ru = models.CharField(max_length=128, db_index=True)
    name_en = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    lon = models.DecimalField(max_digits=10, decimal_places=5)
    okato = models.CharField(max_length=20)

    class Meta:
        db_table = 'sxgeo_cities'

class SxgeoCountry(models.Model):
    iso = models.CharField(max_length=2)
    continent = models.CharField(max_length=2)
    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=6, decimal_places=2)
    lon = models.DecimalField(max_digits=6, decimal_places=2)
    timezone = models.CharField(max_length=30)



    class Meta:
        db_table = 'sxgeo_country'

class SxgeoRegions(models.Model):
    iso = models.CharField(max_length=7)
    country = models.CharField(max_length=2, db_index=True)
    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    timezone = models.CharField(max_length=30)
    okato = models.CharField(max_length=2)
    class Meta:
        db_table = 'sxgeo_regions'





