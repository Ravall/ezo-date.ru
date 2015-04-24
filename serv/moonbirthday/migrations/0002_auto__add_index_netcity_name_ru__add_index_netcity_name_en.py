# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'NetCity', fields ['name_ru']
        db.create_index('net_city', ['name_ru'])

        # Adding index on 'NetCity', fields ['name_en']
        db.create_index('net_city', ['name_en'])


    def backwards(self, orm):
        # Removing index on 'NetCity', fields ['name_en']
        db.delete_index('net_city', ['name_en'])

        # Removing index on 'NetCity', fields ['name_ru']
        db.delete_index('net_city', ['name_ru'])


    models = {
        u'moonbirthday.netcity': {
            'Meta': {'object_name': 'NetCity', 'db_table': "'net_city'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['moonbirthday.NetCountry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
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