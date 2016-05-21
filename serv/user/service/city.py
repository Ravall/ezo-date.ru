# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_geoip.models import IpRange
from django.conf import settings
from moonbirthday.models import SxgeoCities, SxgeoRegions
from django.db import connection


def _get_cityes_not_unic_like_as(city):
    cursor = connection.cursor()
    sql = ( 'select ct.name_ru from sxgeo_cities ct '
        ' join sxgeo_regions rg on ct.`region_id` = rg.id'
        ' where ct.name_ru like "{0}%" group by ct.name_ru having count(*)>1 '.format(city)
    )
    cursor.execute(sql)
    return [x[0] for x in cursor.fetchall()]

def get_city_by_id(id):
    return SxgeoCities.objects.get(pk=id)

def city_like_as(city):
    names_not_unic = _get_cityes_not_unic_like_as(city)
    cursor = connection.cursor()
    sql = ('select ct.name_ru, ct.id, rg.name_ru region_name , cntr.`name_ru` country_name '
        ' from sxgeo_cities ct'
        ' join sxgeo_regions rg on ct.`region_id` = rg.id'
        ' join `sxgeo_country` cntr on cntr.iso = rg.`country`'
        ' where ct.name_ru like "{0}%" '.format(city))
    cursor.execute(sql)
    result_raw = cursor.fetchall()
    return [
        {
            'value':
                obj[0] if obj[0] not in names_not_unic
                else '{0} ({2}, {1})'.format(obj[0],obj[2],obj[3]),
            'data':obj[1]
        } for obj in result_raw]


def get_city(city):
    ## TODO объединить в один запрос
    city = SxgeoCities.objects.get(name_ru=city)
    region = SxgeoRegions.objects.get(pk=city.region_id)
    return {
        'id': city.id,
        'lat':str(city.lat),
        'long':str(city.lon),
        'timezone':str(region.timezone)
    }



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


def is_city_exists(city):
    '''
    проверка на существование города
    '''
    return SxgeoCities.objects.filter(name_ru=city).exclude(region_id=0).exists()

