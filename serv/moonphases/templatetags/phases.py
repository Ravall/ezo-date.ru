# -*- coding: utf-8 -*-
from datetime import datetime
from django import template
from math import ceil

register = template.Library()  #: Django template tag/filter registrator





@register.simple_tag
def img_phase_url(lunation):
    if lunation == 0 or lunation == 1:
        url = 'new_moon'
    elif lunation == 0.5:
        url = 'full_moon'
    elif lunation == 0.25:
        url = 'first_quarter'
    elif lunation == 0.75:
        url = 'third_quarter'
    elif lunation > 0 and lunation < 0.25:
        url = 'waxing_crescent_{0}'.format(int(ceil(lunation / (0.25/6))))
    elif lunation > 0.25 and lunation < 0.5:
        url = 'waxing_gibbous_{0}'.format(int(ceil( (0.5 - lunation) / (0.25/6))))
    elif lunation > 0.5 and lunation < 0.75:
        url = 'waning_gibbous_{0}'.format(int(ceil( (0.75 - lunation) / (0.25/5))))
    elif  lunation > 0.75 and lunation < 1:
        url = 'waning_crescent_{0}'.format(int(ceil( (1 - lunation) / (0.25/6))))
    return '{0}.png'.format(url)


@register.simple_tag
def alt_phase(lunation):
    if lunation == 0 or lunation == 1:
        alt = 'новолуние'
    elif lunation == 0.5:
        alt = 'полнолуние'
    elif lunation == 0.25:
        alt = 'первая четверть'
    elif lunation == 0.75:
        alt = 'последняя четверть'
    elif lunation > 0 and lunation < 0.25:
        alt = 'молодая луна'
    elif lunation > 0.25 and lunation < 0.5:
        alt = 'растущая луна'
    elif lunation > 0.5 and lunation < 0.75:
        alt = 'убывающая луна'
    elif  lunation > 0.75 and lunation < 1:
        alt = 'старая луна'
    return alt