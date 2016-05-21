# -*- coding: utf-8 -*-
from math import sin, pi
from datetime import datetime, timedelta, date
from snct_date.date import (
    date_shift, count_days, yyyy_mm_dd, date_diff, date_compare, month_range
)
import collections


# значиение, когда считаем, что биоритм в пике
PEAK_VALUE = 90
# ключи для графиков
DAY_TYPE_PEAK = 'peak'
DAY_TYPE_GREAT_CRITICAL = 'great_critical_day'
DAY_TYPE_CRITICAL = 'critical_day'
# циклы ритмов
PHYSICAL_PERIOD = 23
EMOTIONAL_PERIOD = 28
BRAIN_PERIOD = 33


def bio(time_diff, period):
    '''
    формула расчетов биоритмов
    '''
    return sin(2 * pi * time_diff / period) * 100


def day_bio(time_diff):
    '''
    значиения биоритмов по всем ритмам
    '''
    return {
        PHYSICAL_PERIOD: bio(time_diff, PHYSICAL_PERIOD),
        EMOTIONAL_PERIOD: bio(time_diff, EMOTIONAL_PERIOD),
        BRAIN_PERIOD: bio(time_diff, BRAIN_PERIOD),
    }


def get_bio_data(birthday_dt, period):
    '''
    получить данные для графиков

    birthday_dt - дата рождения
    period - период, в которым интересны данные
        [0] - дата начала прериода,
        [1] - дата окончания периода
    '''

    return [
        {
            'day': yyyy_mm_dd(
                date_shift(
                    *(birthday_dt + [t,])
                )
            ),
            'fiz': int(bio(t, PHYSICAL_PERIOD)),
            'emo': int(bio(t, EMOTIONAL_PERIOD)),
            'smart': int(bio(t, BRAIN_PERIOD)),
        }
        for t in xrange(
            date_diff(period[0], birthday_dt),
            date_diff(period[1], birthday_dt)+1
        )
    ]

def is_great_critical(critical):
    '''
    оценивает результат функции get_critical_preiods
    и возврщает ture если в выбранный день - великий критический день
    '''
    return (
        len(critical) == 3
        and not reduce(
            lambda res, x: res+(x['type']!='+'), critical, 0
        )
    )


def get_critical_preiods(day, time_diff):
    '''
    критический период - это тот день, в котором
    - отрицательный биоритм переходит в положительный или
    - положительный переходит в отрицательный
    '''
    critical = []
    for period in (EMOTIONAL_PERIOD, PHYSICAL_PERIOD, BRAIN_PERIOD):
        if int(bio(time_diff, period) * bio(time_diff+1, period)) < 0 \
            or int(bio(time_diff, period)) == 0:
            critical.append({
                'period': period,
                # + график возрастает
                # - график убывает
                'type': '+' if int(bio(time_diff+1, period))>0 else '-'
            })

    day_type = (
        DAY_TYPE_GREAT_CRITICAL
        if is_great_critical(critical)
        else DAY_TYPE_CRITICAL
    )
    return {day_type: critical} if critical else {}


def get_peak_preiods(day, time_diff):
    '''
    возвращает флаги пиков ритмов - т.е есть ли в выбранный день пики
    и если есть - то какие
    если пиков нет - возвращает {}
    иначе (например) {
        'peak': [
            {
                period: 23,
                type: '+'
            },
            {
                period: 33,
                type: '-'
            },
        ]


    }
    '''
    critical = []
    for period in (EMOTIONAL_PERIOD, PHYSICAL_PERIOD, BRAIN_PERIOD):
        if abs(int(bio(time_diff, period))) >= PEAK_VALUE:
            critical.append({
                'period': period,
                'type': '+' if int(bio(time_diff, period))>0 else '-'
            })
    return {DAY_TYPE_PEAK: critical} if critical else {}


def git_important_days(birthday_dt, period):
    '''
    получаем список особых дней за указанный период
    birthday_dt - дата рождения
    period - период, в который нужно получить особые даты
        [0] - дата начала прериода,
        [1] - дата окончания периода
    '''
    days = {}
    _day = period[0]
    while date_compare( *(_day+period[1]) )  != -1:
        time_diff = date_diff(_day, birthday_dt)

        critical = get_critical_preiods(_day, time_diff)
        peak = get_peak_preiods(_day, time_diff)
        day = yyyy_mm_dd(_day)

        if (peak or critical):
            days.setdefault(
                day, {
                    'biorythms': day_bio(time_diff),
                    'day': yyyy_mm_dd(_day)
                }
            )
        if peak:
            days[day].update(peak)
        if critical:
            days[day].update(critical)

        _day = date_shift(*(_day + (1,)))
    return collections.OrderedDict(sorted(days.items()))


def get_bio_context(date_bt_tuple, cur_date):
    '''
    возвращает данные по биоритмам для:
    day_bd - дата рождения (d,m,y)
    cur_date - дата для который требуется получить данные по биоритмам
    '''
    period = month_range(cur_date)
    critical_days = git_important_days(date_bt_tuple, period)

    curday_info = {
        'biorythms': day_bio(date_diff(cur_date, date_bt_tuple))
    }
    return {
        'data': get_bio_data(date_bt_tuple, period),
        'today_info': curday_info,
        'critical_info': critical_days.get(yyyy_mm_dd(cur_date), False),
        'critical_days': critical_days
    }

