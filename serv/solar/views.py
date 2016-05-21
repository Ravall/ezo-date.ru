# -*- coding: utf-8 -*-
import json
from datetime import datetime,timedelta
from serv.views import ApiRequestMixin, SessionMixin, FullBirthDayFormMixin
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from solar.service import get_solar_time


class SolarMixin(TemplateView):
    url = ''
    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'solar')
        kwargs.setdefault('url', self.url)
        return super(SolarMixin, self).get_context_data(**kwargs)


class IndexView(ApiRequestMixin, SolarMixin):
    '''
    описание сервиса
    '''
    template_name = "solar/index.html"
    url = 'solar_home'


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['article'] = self.api_get_article('12_vazhnyh_dnyay_so_dnya_rozhdeniya')
        return context


class Days12View(ApiRequestMixin, SolarMixin):
    '''
    список всех дней
    '''
    template_name = "solar/12.html"
    url = 'solar_12'

    def get_context_data(self, **kwargs):
        context = super(Days12View, self).get_context_data(**kwargs)
        context['articles'] = self.api_get_by_tags('solar12')
        return context


class DayView(ApiRequestMixin, SolarMixin):
    '''
    Просмотр статьи о конкретном дне 
    '''
    template_name = "solar/day.html"
    url = 'solar_12'

    def get(self, request, *args, **kwargs):
        num = int(kwargs['nday'])
        if num < 1 or num > 12:
            raise Http404
        return super(DayView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DayView, self).get_context_data(**kwargs)
        context['article'] = self.api_get_article('day_{0}'.format(context['nday']))
        return context


class FormView(FullBirthDayFormMixin, ProcessFormView, SolarMixin, SessionMixin):
    url = 'form'
    template_name = "solar/form.html"

    def form_valid(self, form):
        self.save_to_session(form)
        return HttpResponseRedirect(reverse_lazy('solar_open'))


class OpenView(ApiRequestMixin, SolarMixin, SessionMixin):
    url = 'solar_open'
    template_name = "solar/open.html"

    def get(self, request, *args, **kwargs):
        if not (
            self.get_value('date') and self.get_value('time') and self.get_value('city')
        ):
            return HttpResponseRedirect(reverse_lazy('solar_form'))
        return super(OpenView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(OpenView, self).get_context_data(**kwargs)
        articles = self.api_get_by_tags('solar12')

        b_dt = '{0} {1}'.format(self.get_value('date'), self.get_value('time'))
        b_dt = datetime.strptime(b_dt, '%d.%m.%Y %H:%M')
        city, city_id = self.get_value('city').split('%%')
        year = kwargs.get('year', datetime.today().year)

        solar_open_date = get_solar_time(b_dt, city_id, int(year))
        context['solar_open_time'] = solar_open_date
        context['year'] = year
        
        days = [{
                'date': (solar_open_date+timedelta(days=i), solar_open_date+timedelta(days=i+1)),
                'article': articles[i],
                'current': (datetime.today() >= solar_open_date+timedelta(days=i)
                           and  datetime.today() < solar_open_date+timedelta(days=i+1))
            } for i in range(12)
        ]
        context['days'] = days
        return context
