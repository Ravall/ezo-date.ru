# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
from django.views.generic.edit import ProcessFormView, FormMixin
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from solar.service import get_solar_time
from serv.views import ServiceMixin, LoginRequiredMixin
from user.forms.form import FullBirthdayForm


class SolarService(ServiceMixin):
    service = 'solar'


class IndexView(SolarService):
    template_name = "solar/index.html"
    url = 'solar_home'

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article('12_vazhnyh_dnyay_so_dnya_rozhdeniya')
        }


class Days12View(SolarService):
    template_name = "solar/12.html"
    url = 'solar_12'

    def get_context(self, **kwargs):
        return {
            'articles': self.api_get_by_tags('solar12')
        }


class DayView(SolarService):
    template_name = "solar/day.html"
    url = 'solar_12'

    def get(self, request, *args, **kwargs):
        if not (int(kwargs['nday']) in range(1, 13)):
            raise Http404
        return super(DayView, self).get(request, *args, **kwargs)

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article('day_{0}'.format(kwargs['nday']))
        }


class SolarContext(SolarService):

    def get_db_info(self):
        return {
            'city_id': self.profile.city_id,
            'born_date': self.profile.born_date
        }

    def get_context(self, **kwargs):
        context = {}
        articles = self.api_get_by_tags('solar12')

        year = kwargs.get('year', datetime.today().year)

        solar_info = self.get_db_info()
        if not solar_info:
            return {}
        solar_open_date = get_solar_time(solar_info['born_date'], solar_info['city_id'], int(year))
        context['solar_open_time'] = solar_open_date
        context['year'] = year

        days = [{
            'date': (solar_open_date + timedelta(days=i), solar_open_date + timedelta(days=i + 1)),
            'article': articles[i],
            'current': (datetime.today() >= solar_open_date + timedelta(days=i)
                        and datetime.today() < solar_open_date + timedelta(days=i + 1))
        } for i in range(12)]
        context['days'] = days
        return context


class FormView(ProcessFormView, FormMixin, SolarContext):
    url = 'form'
    template_name = "solar/form.html"
    form_class = FullBirthdayForm

    def get_db_info(self):
        solar = self.request.session.pop('solar', False)
        if solar:
            solar['born_date'] = datetime.strptime(solar['born_date'], '%Y-%m-%d %H:%M')
            self.template_name = "solar/form_result.html"
        return solar

    def form_valid(self, form):
        self.request.session['solar'] ={
            'born_date':  ':'.join(form.get_bd().isoformat(" ").split(':')[:2]),
            'city_id': form.get_city_id(self.request)
        }
        return HttpResponseRedirect(reverse_lazy('solar_form'))


class OpenView(LoginRequiredMixin, SolarContext):
    url = 'solar_open'
    template_name = "solar/open.html"

