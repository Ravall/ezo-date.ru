# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NetCountry'
        db.create_table('net_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCountry'])

        # Adding model 'NetCity'
        db.create_table('net_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCountry'])),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCity'])

        # Adding model 'NetCityIp'
        db.create_table('net_city_ip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCity'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCityIp'])

        # Adding model 'NetCountryIp'
        db.create_table('net_country_ip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCountry'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetCountryIp'])

        # Adding model 'NetEuro'
        db.create_table('net_euro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCountry'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetEuro'])

        # Adding model 'NetRu'
        db.create_table('net_ru', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moonbirthday.NetCity'])),
            ('begin_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('end_ip', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'moonbirthday', ['NetRu'])


    def backwards(self, orm):
        # Deleting model 'NetCountry'
        db.delete_table('net_country')

        # Deleting model 'NetCity'
        db.delete_table('net_city')

        # Deleting model 'NetCityIp'
        db.delete_table('net_city_ip')

        # Deleting model 'NetCountryIp'
        db.delete_table('net_country_ip')

        # Deleting model 'NetEuro'
        db.delete_table('net_euro')

        # Deleting model 'NetRu'
        db.delete_table('net_ru')


    models = {
        u'moonbirthday.netcity': {
            'Meta': {'object_name': 'NetCity', 'db_table': "'net_city'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['moonbirthday.NetCountry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        u'moonbirthday.netcityip': {
            'Meta': {'object_name': 'NetCityIp', 'db_table': "'net_city_ip'"},
            'begin_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['moonbirthday.NetCity']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'moonbirthday.netcountry': {
            'Meta': {'object_name': 'NetCountry', 'db_table': "'net_country'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'moonbirthday.netcountryip': {
            'Meta': {'object_name': 'NetCountryIp', 'db_table': "'net_country_ip'"},
            'begin_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['moonbirthday.NetCountry']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'moonbirthday.neteuro': {
            'Meta': {'object_name': 'NetEuro', 'db_table': "'net_euro'"},
            'begin_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['moonbirthday.NetCountry']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'moonbirthday.netru': {
            'Meta': {'object_name': 'NetRu', 'db_table': "'net_ru'"},
            'begin_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['moonbirthday.NetCity']"}),
            'end_ip': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['moonbirthday']