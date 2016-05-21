# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from datetime import datetime

register = template.Library()  #: Django template tag/filter registrator


@register.inclusion_tag('user/templatetags/year_navigator.html')
def year_navigator(route, year=None):
    year = int(year) or datetime.today().year
    return {
        'route': route,
        'current': year,
        'years': range(year - 2, year + 3),
        'prev': year - 1,
        'next': year + 1,
    }