# -*- coding: utf-8 -*-
import ephem
from math import ceil
from moonbirthday.service import get_geo_by_cityid, _to_utc, _to_local
from datetime import datetime


def get_moon_day_by_cityid(city_id, dt=False):
    '''
    возвращает лунный деньнь по city_id
    '''
    geo = get_geo_by_cityid(city_id)
    return get_moon_day_by_geo(geo, dt)


def get_moon_day_by_geo(geo, my_dt=False):
    '''
    возвращает лунный день по гео массиву
    '''
    ob = ephem.Observer()
    ob.lat = geo['lat']
    ob.long = geo['long']
    ob.date = ephem.Date(_to_utc(geo['timezone'], my_dt))
    ob_date = ob.date
    new_moon = ephem.previous_new_moon(ob.date)

    try:
        dt = new_moon
        moon_bithday = 0
        for i in range(1,31):
            moon_bithday += 1
            ob.date = dt
            dt = ob.next_rising(ephem.Moon())
            if _to_local(geo['timezone'], dt.datetime()) > my_dt:
                break
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        moon_bithday  = int(ceil(ob_date - new_moon))
    return moon_bithday


def get_periods(dt, geo):
    def loc(date):
        return _to_local(geo['timezone'], date.datetime())

    ob = ephem.Observer()
    ob.lat = geo['lat']
    ob.long = geo['long']
    ob.date = ephem.Date(_to_utc(geo['timezone'], dt))

    # начало-конец текущего лунного дня
    try:
        # конец дня
        end_day = ob.next_rising(ephem.Moon())
        if end_day > ephem.next_new_moon(ob.date):
            # если конец дня посчитался после новолуния 
            # то конец дня - будет начало новолуния
            end_day = ephem.next_new_moon(ob.date)
        # начало дня
        begin_day = ob.previous_rising(ephem.Moon())
        if begin_day < ephem.previous_new_moon(ob.date):
            # если начало дня раньше новолуния
            # то начало дня это предыдущее новолуние
            begin_day = ephem.previous_new_moon(ob.date)

    except (ephem.NeverUpError, ephem.AlwaysUpError):

        new_moon = ephem.previous_new_moon(ob.date)
        moon_count = int(ceil(ob_date - new_moon))

        begin_day = ephem.date(moon_month_begin + (moon_count - 1) * moon_day_long * ephem.second)
        end_day = ephem.date(moon_month_begin + moon_count * moon_day_long * ephem.second)


    # начало лунного месяца
    moon_month_begin = ephem.previous_new_moon(ob.date)
    ob.date = moon_month_begin
    #конец лунного месяца
    moon_month_end = ephem.next_new_moon(ob.date)
    # средняя продолжительность лунного дня
    moon_day_long = ((moon_month_end - moon_month_begin)*24*60*60)/30


    # конец первого лунного дня - восход луны после новолуния
    try:
        end_new_moon = ob.next_rising(ephem.Moon())
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        end_new_moon = ephem.date(moon_month_begin + moon_day_long * ephem.second)

    # полнолуние
    full_moon = ephem.next_full_moon(ob.date)


    try:
        ob.date = full_moon
        # конец полнолуния
        end_full_moon = ob.next_rising(ephem.Moon())
        # начало дня
        begin_full_moon = ob.previous_rising(ephem.Moon())
    except (ephem.NeverUpError, ephem.AlwaysUpError):
        begin_full_moon = ephem.date(moon_month_begin + 14 * moon_day_long * ephem.second)
        end_full_moon = ephem.date(moon_month_begin + 15 * moon_day_long * ephem.second)

    


    return {

        'this_day': (loc(begin_day), loc(end_day)),
        'new': (loc(moon_month_begin), loc(end_new_moon)),
        'waxing': (loc(end_new_moon),loc(begin_full_moon)),
        'full': (loc(begin_full_moon),loc(end_full_moon)),
        'waning': (loc(end_full_moon), loc(moon_month_end)),
        'next_day': loc(ephem.date( moon_month_end + ephem.hour )),
        'prev_day': loc(ephem.date( moon_month_begin - ephem.hour ))
    }


def what_period(periods, dt):
    if dt < periods['new'][0] or dt > periods['waning'][1]:
        alt = 'unknown'
    elif dt >=  periods['full'][0] and dt <= periods['full'][1]:
        alt = 'full'
    elif dt >=  periods['new'][0] and dt <= periods['new'][1]:
        alt = 'new'
    elif dt < periods['full'][0]:
        alt = 'waxing'
    elif dt > periods['full'][1]:
        alt = 'waning'
    else:
        alt = 'unknown'
    return alt


def get_moonday_info(dt, geo, is_show_add_periods=True):
    """
    Возвращает информацию о дне
    Returns a floating-point number from 0-1.
    where 0=new, 0.5=full, 1=new """
    date = ephem.Date(_to_utc(geo['timezone'], dt))
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    nfm = ephem.next_full_moon(date)
    pfm = ephem.previous_full_moon(date)

    ob = ephem.Observer()
    ob.lat = geo['lat']
    ob.long = geo['long']
    ob.date = date
    try:
        prm = ob.previous_rising(ephem.Moon())
        prm_date = _to_local(geo['timezone'], prm.datetime())
    except ephem.NeverUpError:
        prm_date = 'NeverUp'
    except ephem.AlwaysUpError:
        prm_date = 'AlwaysUp'

    try:
        nsm = ob.next_setting(ephem.Moon())
        nsm_date = _to_local(geo['timezone'], nsm.datetime())
    except ephem.NeverUpError:
        nsm_date = 'NeverUp'
    except ephem.AlwaysUpError:
        nsm_date = 'AlwaysUp'

    # переведем в местное время
    pnm_date = _to_local(geo['timezone'], pnm.datetime())
    nnm_date = _to_local(geo['timezone'], nnm.datetime())
    nfm_date = _to_local(geo['timezone'], nfm.datetime())
    pfm_date = _to_local(geo['timezone'], pfm.datetime())
    if nnm < nfm:
        # если следующее событие - новолуние,
        # а не полнолуние, то луна убывающая
        # > 0.5
        lunation = 1 - (
            ((nnm_date - dt).total_seconds()) / ((nnm_date - pfm_date).total_seconds())
        ) * 0.5
    if nfm < nnm:
        # если следующее событие - полнолуние,
        # а не новолуние, то луна растущая
        # < 0.5
        lunation = 0.5 - (
            ((nfm_date - dt).total_seconds()) / ((nfm_date - pnm_date).total_seconds())
        ) * 0.5


    moon_day = get_moon_day_by_geo(geo, dt)
    moon = ephem.Moon(date)
    # периоды этого лунного месяца
    periods = get_periods(dt, geo)

    result = {
        'today': what_period(periods, dt),
        # периоды этого лунного месяца
        'periods': periods,
        'moon_phase': moon.moon_phase,
        'next_full_moon': nfm_date,
        'previous_full_moon': pfm_date,
        'next_new_moon': nnm_date,
        'previous_new_moon': pnm_date,
        'lunation': lunation,
        'previous_rising': prm_date,
        'next_setting': nsm_date,
        'moon_day': moon_day,
    }

    if is_show_add_periods:
        # периоды следующего лунного месяца
        next_periods = get_periods(periods['next_day'], geo)
        # периоды предыдущего лунного месяца 
        previous_periods = get_periods(periods['prev_day'], geo)
        # периоды следующего лунного месяца
        result['next_periods'] = next_periods
        # периоды предыдущего лунного месяца 
        result['previous_periods'] = previous_periods

    return result
    


   


def get_moon_bithday(my_dt, city_id):
    '''
    лунный день рождения
    '''
    geo = get_geo_by_cityid(city_id)
    ob = ephem.Observer()
    ob.lat = geo['lat']
    ob.long = geo['long']
    ob.date = ephem.Date(_to_utc(geo['timezone'], my_dt))
    new_moon = ephem.previous_new_moon(ob.date)
    dt = new_moon
    moon_bithday = 0
    for i in range(1,31):
        moon_bithday += 1
        ob.date = dt
        dt = ob.next_rising(ephem.Moon())
        if _to_local(geo['timezone'], dt.datetime()) > my_dt:
            break
    return moon_bithday