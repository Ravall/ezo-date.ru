# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytz
from datetime import datetime
import ephem
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from moonbirthday.models import SxgeoCities, SxgeoRegions
from django_geoip.models import IpRange


def get_city(city):
    ## TODO объединить в один запрос
    city = SxgeoCities.objects.get(name_ru=city)
    region = SxgeoRegions.objects.get(pk=city.region_id)
    return {
        'id': city.id,
        'lat':str(city.lat),
        'long':str(city.lon),
        'timezone':str(region.timezone),
    }


def get_city_by_id(city_id):
    try:
        city = SxgeoCities.objects.get(pk=city_id)
        city_name = city.name_ru
    except:
        city_id = False,
        city_name = False
    return city_name, city_id


def get_default_city(ip):
    try:
        geoip_record = IpRange.objects.by_ip(ip)
        city = geoip_record.city
        city_data = get_city(city)
        city_id = city_data['id']
    except:
        city = settings.MOONBIRTHDAY['default_city']
        city_id = settings.MOONBIRTHDAY['default_city_id']
    return city, city_id


def get_cityes_not_unic_like_as(city):
    cursor = connection.cursor()
    sql = ( 'select ct.name_ru from sxgeo_cities ct '
        ' join sxgeo_regions rg on ct.`region_id` = rg.id and rg.country = "RU" '
        ' where ct.name_ru like "{0}%" group by ct.name_ru having count(*)>1 '.format(city)
    )
    cursor.execute(sql)
    return [x[0] for x in cursor.fetchall()]



def city_like_as(city):
    names_not_unic = get_cityes_not_unic_like_as(city)
    cursor = connection.cursor()
    sql = ('select ct.name_ru, ct.id, rg.name_ru region_name from sxgeo_cities ct'
        ' join sxgeo_regions rg on ct.`region_id` = rg.id and rg.country = "RU"'
        ' where ct.name_ru like "{0}%" '.format(city))
    cursor.execute(sql)
    result_raw = cursor.fetchall()
    return [
        {
            'value':
                obj[0] if obj[0] not in names_not_unic
                else '{0} ({1})'.format(obj[0],obj[2]),
            'data':obj[1]
        } for obj in result_raw]



def is_city_exists(city):
    return SxgeoCities.objects.filter(name_ru=city).exclude(region_id=0).exists()



def get_geo_by_cityid(city_id):
    cursor = connection.cursor()
    sql = (
        'SELECT '
        'sx_c.id, sx_c.name_ru city_name, sx_c.`region_id`, '
        'sx_r.`name_ru` region_name,  sx_c.`lat`,sx_c.`lon`, '
        'sx_r.`timezone` '
        'FROM `sxgeo_cities` sx_c '
        'JOIN `sxgeo_regions` sx_r ON sx_r.id = sx_c.region_id '
        'WHERE sx_c.id = {0}'.format(city_id)
    )
    cursor.execute(sql)
    result_raw = cursor.fetchall()
    if not result_raw:
        return False
    return {
        'lat':str(result_raw[0][4]),
        'long':str(result_raw[0][5]),
        'timezone':str(result_raw[0][6]),
    }

def _to_local(tz, dt):
    local_tz = pytz.timezone(tz)
    local_dt = dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt).replace(tzinfo=None)

def _to_utc(tz, l_dt):
    local_tz = pytz.timezone(tz)
    dt = local_tz.localize(l_dt)
    return dt.astimezone(pytz.UTC)

