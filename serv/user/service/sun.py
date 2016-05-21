# -*- coding: utf-8 -*-
import ephem
from moonbirthday.service import _to_utc, _to_local
from datetime import timedelta, datetime, time


def get_sun_info(dt, geo):

    # начало дня
    day_00_00 = datetime.combine(dt.date(),time(0,0))

    date = ephem.Date(_to_utc(geo['timezone'], day_00_00))

    ob = ephem.Observer()
    ob.lat = geo['lat']
    ob.long = geo['long']
    ob.date = date

    # восход солцна
    rising = ob.next_rising(ephem.Sun())
    rising_time = _to_local(geo['timezone'], rising.datetime())
    # закат солнца
    setting = ob.next_setting(ephem.Sun())
    setting_time = _to_local(geo['timezone'], setting.datetime()) 
    # продолжительность дня
    day_long = (setting_time - rising_time).total_seconds()
    # истинный полдень
    sun_noon = rising_time + timedelta(seconds=day_long/2)
    # разница между истинным полднем и общепринятым в 12:00
    diff = sun_noon - datetime.combine(datetime.today(), time(12,0))

    # расчитаем реально время сна, подъема, завтрака и обеда
    time_to_sleep = datetime.combine(datetime.today(), time(22,0)) + diff
    time_to_wakeup = datetime.combine(datetime.today(), time(6,0)) + diff
    time_to_lunch = datetime.combine(datetime.today(), time(12,0)) + diff
    time_to_dinner = datetime.combine(datetime.today(), time(17,0)) + diff



    return {
        'rising': rising_time,
        'setting': setting_time,
        'sun_noon': sun_noon,
        'time_to_sleep':time_to_sleep,
        'time_to_wakeup':time_to_wakeup,
        'time_to_lunch':time_to_lunch,
        'time_to_dinner':time_to_dinner,
        'diff_second': int(diff.total_seconds()),
        'diff_datetime': timedelta(seconds=diff.seconds),
    }