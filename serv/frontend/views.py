# -*- coding: utf-8 -*-
import json
from serv.views import SessionMixin
from django.views.generic import TemplateView
from serv.service import api_request
import calendar
import datetime
from moonbirthday.service import get_default_city
from moonbirthday.service import get_geo_by_cityid
from user.service.moon import get_moonday_info
from user.service.sun import get_sun_info


calendar.month_name = calendar._localized_month("%OB,")


class MyHtmlCalendar(calendar.LocaleHTMLCalendar):
    
    
    def __init__(self, firstweekday, locale):
        self.today = datetime.date.today()
        return super(MyHtmlCalendar, self).__init__(firstweekday, locale)


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




class Index(TemplateView, SessionMixin):
    template_name = "frontend/promo.html"

    def get_city(self):
        value = self.get_value('city_live')
        if value:
            city, city_id = value.split('%%')
        else:
            city, city_id = get_default_city(self.request.META['REMOTE_ADDR'])
        return city, city_id



    def get_context_data(self, **kwargs):
        myCal = MyHtmlCalendar(calendar.MONDAY, 'ru_RU')
        clndr =  myCal.formatmonth()


        city, city_id = self.get_city()
        geo = get_geo_by_cityid(city_id)


        now = datetime.datetime.now()
        moon_info =  get_moonday_info(now, geo)
        sun_info = get_sun_info(now, geo)


        return {
            'now': now,
            'moon_info': moon_info,
            'sun_info': sun_info,
            'calendar': clndr
        }

