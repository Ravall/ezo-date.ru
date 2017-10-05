# -*- coding: utf-8 -*-
import ephem
from moonbirthday.service import get_geo_by_cityid, _to_utc
from datetime import datetime, timedelta, time

def get_sun_angle(dt, geo):
    ob = ephem.Observer()
    ob.lat = geo['lat']
    ob.lon = geo['long']
    ob.date = ephem.Date(_to_utc(geo['timezone'], dt))
    sun = ephem.Sun(ob)
    return sun.ra


def get_solar_time(birthday_dt, city_id, year):

    geo = get_geo_by_cityid(city_id)
    today_birthday = birthday_dt.replace(year=year)

    dd = today_birthday
    d_1 = datetime.combine(dd.date(), datetime.min.time())
    d_2 = datetime.combine(dd.date(), datetime.max.time())

    def a_cmp(d1, d2, bdt, g):
        return not (
            (get_sun_angle(d2, g) < get_sun_angle(bdt, g)) or (get_sun_angle(d1, g) > get_sun_angle(bdt, g))
        )

    count = 0
    while not a_cmp(d_1, d_2, birthday_dt, geo):

        sign = 0
        # если угол солнца в день рождения больше чем конец дня - то смотрим след день
        if get_sun_angle(d_2, geo) < get_sun_angle(birthday_dt, geo):
            sign = 1
        # если угол солнца в день рождения меньше  чем начало дня - то смотрим пред день день
        if get_sun_angle(d_1, geo) > get_sun_angle(birthday_dt, geo):
            sign = -1

        if sign == 0:
            # для порядку, но такого быть не должно
            break

        dd = dd + timedelta(days=sign)
        d_1 = datetime.combine(dd.date(), datetime.min.time())
        d_2 = datetime.combine(dd.date(), datetime.max.time())

        # на всяки случай, но такого быть не должно
        count += 1
        if count > 1000:
            raise Exception('bug! loop too mach')

    # подберем час
    for h in range(24):

        d_1 = datetime.combine(dd.date(),time(h, 0, 0, 0))
        d_2 = datetime.combine(dd.date(),time(h, 59, 59, 999999))
        dd = d_1
        if a_cmp(d_1, d_2, birthday_dt, geo):
            break
            
    # подберем минуту
    for m in range(60):

        d_1 = datetime.combine(dd.date(), time(h, m, 0, 0))
        d_2 = datetime.combine(dd.date(), time(h, m, 59, 999999))
        dd = d_1
        if a_cmp(d_1, d_2, birthday_dt, geo):
            break
    return dd




