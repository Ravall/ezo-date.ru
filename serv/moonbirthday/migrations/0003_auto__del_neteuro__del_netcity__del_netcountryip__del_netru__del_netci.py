# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):


    def forwards(self, orm):
        # Deleting model 'NetEuro'
        db.delete_table('net_euro')

        # Deleting model 'NetCity'
        db.delete_table('net_city')

        # Deleting model 'NetCountryIp'
        db.delete_table('net_country_ip')

        # Deleting model 'NetRu'
        db.delete_table('net_ru')

        # Deleting model 'NetCityIp'
        db.delete_table('net_city_ip')

        # Deleting model 'NetCountry'
        db.delete_table('net_country')

        # Adding model 'SxgeoRegions'
        db.create_table('sxgeo_regions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('okato', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'moonbirthday', ['SxgeoRegions'])

        # Adding model 'SxgeoCountry'
        db.create_table('sxgeo_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('continent', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'moonbirthday', ['SxgeoCountry'])

        # Adding model 'SxgeoCities'
        db.create_table('sxgeo_cities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=5)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=5)),
            ('okato', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'moonbirthday', ['SxgeoCities'])


    def backwards(self, orm):
        # Adding model 'NetEuro'
        db.create_table('net_euro', (
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCountry'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetEuro'])

        # Adding model 'NetCity'
        db.create_table('net_city', (
            ('name_ru', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100, db_index=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCountry'])),
            ('name_en', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100, db_index=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCity'])

        # Adding model 'NetCountryIp'
        db.create_table('net_country_ip', (
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCountry'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCountryIp'])

        # Adding model 'NetRu'
        db.create_table('net_ru', (
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCity'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetRu'])

        # Adding model 'NetCityIp'
        db.create_table('net_city_ip', (
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCity'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCityIp'])

        # Adding model 'NetCountry'
        db.create_table('net_country', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCountry'])

        # Deleting model 'SxgeoRegions'
        db.delete_table('sxgeo_regions')

        # Deleting model 'SxgeoCountry'
        db.delete_table('sxgeo_country')

        # Deleting model 'SxgeoCities'
        db.delete_table('sxgeo_cities')


    models = {
        u'moonbirthday.sxgeocities': {
            'Meta': {'object_name': 'SxgeoCities', 'db_table': "'sxgeo_cities'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'okato': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'moonbirthday.sxgeocountry': {
            'Meta': {'object_name': 'SxgeoCountry', 'db_table': "'sxgeo_country'"},
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
            'Meta': {'object_name': 'SxgeoRegions', 'db_table': "'sxgeo_regions'"},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'okato': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['moonbirthday']