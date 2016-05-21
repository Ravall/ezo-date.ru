# -*- coding: utf-8 -*-
from datetime import datetime
from django import template
from math import ceil
from time import strftime
from snct_date.date import sancta_datefrormat

register = template.Library()  #: Django template tag/filter registrator


@register.simple_tag
def img_phase_url(moon_info):
    lunation = moon_info['lunation']
    if moon_info['today'] == 'new':
        url = 'new_moon'
    elif moon_info['today'] == 'full':
        url = 'full_moon'
    elif lunation == 0.25:
        url = 'first_quarter'
    elif lunation == 0.75:
        url = 'third_quarter'
    elif lunation > 0 and lunation < 0.25:
        url = 'waxing_crescent_{0}'.format(int(ceil(lunation / (0.25/6))))
    elif lunation > 0.25 and lunation < 0.5:
        url = 'waxing_gibbous_{0}'.format(7 - int(ceil( (0.5 - lunation) / (0.25/6))))
    elif lunation > 0.5 and lunation < 0.75:
        url = 'waning_gibbous_{0}'.format(6 - int(ceil( (0.75 - lunation) / (0.25/5))))
    elif  lunation > 0.75 and lunation < 1:
        url = 'waning_crescent_{0}'.format(7-int(ceil( (1 - lunation) / (0.25/6))))
    return '{0}.png'.format(url)


@register.simple_tag
def alt_phase_lunation(lunation):
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


@register.simple_tag
def alt_phase_period(period):
    return {
        'unknown': 'обработка...',
        'full': 'полнолуние',
        'new': 'новолуние',
        'waxing': 'растущая луна',
        'waning': 'убывающая луна'
    }[period]


@register.filter
def cross_gorizont_error_text(time):
    if time == 'NeverUp':
        time = 'в этот день не восходит'
    if time == 'AlwaysUp':
        time = 'в этот день не заходит'
    return time


@register.simple_tag
def phase_time(moon_info, period, phase):
    return 'c {0}&nbsp;{1} по&nbsp;{2}&nbsp;{3}'.format(
        sancta_datefrormat(moon_info[period][phase][0], "[d]&nbsp;[M2]"),
        moon_info[period][phase][0].strftime("%H:%M"),
        sancta_datefrormat(moon_info[period][phase][1], "[d]&nbsp;[M2]"),
        moon_info[period][phase][1].strftime("%H:%M"),
    )