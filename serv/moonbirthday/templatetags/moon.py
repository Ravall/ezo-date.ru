# -*- coding: utf-8 -*-
from django import template


register = template.Library()  #: Django template tag/filter registrator


@register.filter
def url_to_digit(url):
    return int(url.split('_')[0])


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.filter(name='item')
def item(value, i):
    return value[i]


@register.filter(name='next')
def next(value):
    '''
    id_city_live_0 -> id_city_live_1
    '''
    path = value.split('_')
    path[-1] = str(int(path[-1])+1)
    return '_'.join(path)
