from django.views.generic import TemplateView
from serv.views import ApiRequestMixin, SessionMixin
from user.service.moon import get_moonday_info, get_periods
from django.views.generic.edit import ProcessFormView
from serv.views import CityFormMixin
import datetime
from moonbirthday.service import get_default_city, get_geo_by_cityid
import calendar
import re
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy


calendar.month_name = calendar._localized_month("%OB,")


class MyHtmlCalendar(calendar.LocaleHTMLCalendar):
    

    def __init__(self, firstweekday, locale, moon_info):
        self.moon_info = moon_info
        self.today = datetime.date.today()
        return super(MyHtmlCalendar, self).__init__(firstweekday, locale)

    def formatday(self, day, weekday):

        add_css_class = False
        

        if day == self.today.day:
            add_css_class = 'today'
        elif day == self.moon_info['periods']['new'][0].day:
            add_css_class = 'new'
        elif day == self.moon_info['periods']['full'][0].day:
            add_css_class = 'full'

        if day>0:
            html = '<td class="{0} {1}"><a href="#" day="{3}" class="moonphases_day">{2}</a></td>'.format (
                self.cssclasses[weekday], add_css_class, 
                day, self.today.replace(day=day)
            )
        else:
            html =  super(MyHtmlCalendar, self).formatday(day, weekday)
        return html


    def formatmonth(self, theyear=None, themonth=None, withyear=True):
        if theyear is None:
            theyear = self.today.year
        if themonth is None:
            themonth = self.today.month
        return super(MyHtmlCalendar, self).formatmonth(theyear, themonth, withyear)



class MoonPhasesMixin(TemplateView, SessionMixin):
    url = ''

    def get_context_data(self, **kwargs):
        
        now = datetime.datetime.now()
        city, city_id = self.get_city()
        geo = get_geo_by_cityid(city_id)

        moon_info =  get_moonday_info(now, geo)

        kwargs.setdefault('now', now)
        kwargs.setdefault('moon_info', moon_info)
        kwargs.setdefault('service', 'moonphases')
        kwargs.setdefault('url', self.url)

        kwargs.setdefault('city',  re.sub('\(.*\)', '', city).strip())

        self.geo = geo

      
        return super(MoonPhasesMixin, self).get_context_data(**kwargs)


    def get_city(self):
        value = self.get_value('city_live')
        if value:
            city, city_id = value.split('%%')
        else:
            city, city_id = get_default_city(self.request.META['REMOTE_ADDR'])
        return city, city_id



class IndexView(MoonPhasesMixin):
    url = 'moonphases_home'
    template_name = "moonphases/index.html"


class MoonPhasesArticles(ApiRequestMixin, MoonPhasesMixin):
    url = 'moonphases_articles'
    template_name = "moonphases/articles.html"   

    def get_context_data(self, **kwargs):
        context = super(MoonPhasesArticles, self).get_context_data(**kwargs)
        context['articles'] = self.api_get_by_tags('moon_phases')
        return context 


class MoonPhasesMyCity(CityFormMixin, ProcessFormView, MoonPhasesMixin, SessionMixin):
    template_name = "moonphases/city.html"
    url = 'form'

    def form_valid(self, form):
        self.save_to_session(form)
        return HttpResponseRedirect(reverse_lazy('moonphases_home'))



class Article(ApiRequestMixin, MoonPhasesMixin):
    url = 'moonphases_articles'
    template_name = "moonphases/article.html"   

    def get_context_data(self, **kwargs):
        context = super(Article, self).get_context_data(**kwargs)
        context['article'] = self.api_get_article(context['artname'])
        return context 
        
   

class MonthView(ApiRequestMixin, MoonPhasesMixin):
    url = 'moonphases_month'
    template_name = "moonphases/month.html"


    def get_context_data(self, **kwargs):
        context = super(MonthView, self).get_context_data(**kwargs)
        first_day = context['now'].replace(
            day=1, hour=0, second=0, minute=0, microsecond=0
        )
        day = first_day
        mooon_month = []
        while day.month == context['now'].month:
            info =  get_moonday_info(day, self.geo, False)
            mooon_month.append(info)
            day = info['periods']['this_day'][1] + datetime.timedelta(seconds=1)
        context['mooon_month'] = mooon_month
        return context




