# -*- coding: utf-8 -*-
import re
from serv.views import ApiRequestMixin, SessionMixin
from django.views.generic import TemplateView
from serv.views import CityFormMixin
from django.views.generic.edit import ProcessFormView
from user.service.sun import get_sun_info
from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from moonbirthday.service import get_default_city, get_geo_by_cityid



class SuntimeMixin(TemplateView, SessionMixin):
    url = ''
    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'suntime')
        kwargs.setdefault('url', self.url)

        city, city_id = self.get_city()
        kwargs.setdefault('city',  re.sub('\(.*\)', '', city).strip())

        geo = get_geo_by_cityid(city_id)
        now = datetime.now()
        kwargs.setdefault('sun_info', get_sun_info(now, geo))
        
        return super(SuntimeMixin, self).get_context_data(**kwargs)

    def get_city(self):
        value = self.get_value('city_live')
        if value:
            city, city_id = value.split('%%')
        else:
            city, city_id = get_default_city(self.request.META['REMOTE_ADDR'])
        return city, city_id


class IndexView(SuntimeMixin):
    template_name = 'suntime/index.html'
    url  = 'suntime_home'


class ArticlesView(ApiRequestMixin, SuntimeMixin):
    template_name = 'suntime/articles.html'
    url  = 'suntime_articles'

    def get_context_data(self, **kwargs):
        context = super(ArticlesView, self).get_context_data(**kwargs)
        context['articles'] = self.api_get_by_tags('suntime')
        return context 


class ArticleView(ApiRequestMixin, SuntimeMixin):
    template_name = 'suntime/article.html'
    url  = 'suntime_articles'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['article'] = self.api_get_article(context['artname'])
        return context 
        



class ChangeCity(CityFormMixin, ProcessFormView, SuntimeMixin):
    template_name = "suntime/city.html"
    url = 'form'

    def form_valid(self, form):
        self.save_to_session(form)
        return HttpResponseRedirect(reverse_lazy('suntime_home'))



