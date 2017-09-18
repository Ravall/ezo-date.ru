# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
import calendar
import datetime
from moonbirthday.service import get_geo_by_cityid
from user.service.moon import get_moonday_info
from user.service.sun import get_sun_info
from serv.views import CityLiveMixin


class MyHtmlCalendar(calendar.LocaleHTMLCalendar):
    def __init__(self, firstweekday, locale):
        self.today = datetime.date.today()
        super(MyHtmlCalendar, self).__init__(firstweekday, locale)

    def formatday(self, day, weekday):
        if day != self.today.day:
            return super(MyHtmlCalendar, self).formatday(day, weekday)
        else:
            return '<td class="%s today">%d</td>' % (self.cssclasses[weekday], day)

    def formatmonth(self, theyear=None, themonth=None, withyear=True):
        if theyear is None:
            theyear = self.today.year
        if themonth is None:
            themonth = self.today.month
        return super(MyHtmlCalendar, self).formatmonth(theyear, themonth, withyear)


class Index(TemplateView, CityLiveMixin):
    template_name = "frontend/promo.html"

    def get_context_data(self, **kwargs):
        myCal = MyHtmlCalendar(calendar.MONDAY, 'ru_RU.UTF-8')
        clndr = myCal.formatmonth()
        city, city_id = self.get_city()
        geo = get_geo_by_cityid(city_id)
        moon_info =  get_moonday_info(self.now, geo)
        sun_info = get_sun_info(self.now, geo)
        return {
            'now': self.now,
            'moon_info': moon_info,
            'sun_info': sun_info,
            'calendar': clndr
        }

