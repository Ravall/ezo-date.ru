# -*- coding: utf-8 -*-
from django import template


register = template.Library()  #: Django template tag/filter registrator


@register.filter
def url_to_digit(url):
    return int(url.split('_')[0])


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)