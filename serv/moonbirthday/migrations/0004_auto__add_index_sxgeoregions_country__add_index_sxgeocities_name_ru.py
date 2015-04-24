# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):


    def forwards(self, orm):
        # Adding index on 'SxgeoRegions', fields ['country']
        db.create_index(u'sxgeo_regions', ['country'])

        # Adding index on 'SxgeoCities', fields ['name_ru']
        db.create_index(u'sxgeo_cities', ['name_ru'])


    def backwards(self, orm):
        # Removing index on 'SxgeoCities', fields ['name_ru']
        db.delete_index(u'sxgeo_cities', ['name_ru'])

        # Removing index on 'SxgeoRegions', fields ['country']
        db.delete_index(u'sxgeo_regions', ['country'])


    models = {
        u'moonbirthday.sxgeocities': {
            'Meta': {'object_name': 'SxgeoCities', 'db_table': "u'sxgeo_cities'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'okato': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'moonbirthday.sxgeocountry': {
            'Meta': {'object_name': 'SxgeoCountry', 'db_table': "u'sxgeo_country'"},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'moonbirthday.sxgeoregions': {
            'Meta': {'object_name': 'SxgeoRegions', 'db_table': "u'sxgeo_regions'"},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'okato': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['moonbirthday']