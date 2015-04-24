# -*- coding: utf-8 -*-
from datetime import datetime
from django import template


register = template.Library()  #: Django template tag/filter registrator


@register.filter
def url_to_num(url):
    return int(url.split('_')[1])

@register.simple_tag
def past_future(word_in_past, word_in_future, time):
    return word_in_past if time < datetime.today() else word_in_future