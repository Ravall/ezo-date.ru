# -*- coding: utf-8 -*-
import ephem
from moonbirthday.service import _to_local, _to_utc


def get_moonday_info(dt, geo):
  """ Returns a floating-point number from 0-1.
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

  prm = ob.previous_rising(ephem.Moon())
  nsm = ob.next_setting(ephem.Moon())

  lunation = (date - pnm) / (nnm - pnm)
  #Note that there is a ephem.Moon().phase() command, but this returns the
  #percentage of the moon which is illuminated. This is not really what we want.

  dtt = pnm
  moon_day = 0
  for i in range(1,31):
      moon_day += 1
      ob.date = dtt
      dtt = ob.next_rising(ephem.Moon())
      if _to_local(geo['timezone'], dtt.datetime()) > dt:
          break

  return {
      'next_full_moon': _to_local(geo['timezone'], nfm.datetime()),
      'previous_full_moon': _to_local(geo['timezone'], pfm.datetime()),
      'next_new_moon': _to_local(geo['timezone'], nnm.datetime()),
      'previous_new_moon': _to_local(geo['timezone'], pnm.datetime()),
      'lunation': lunation,
      'previous_rising': _to_local(geo['timezone'], prm.datetime()),
      'next_setting': _to_local(geo['timezone'], nsm.datetime()),
      'moon_day': moon_day,
  }


