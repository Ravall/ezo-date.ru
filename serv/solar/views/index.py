# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView, FormMixin
from django.http import HttpResponseRedirect
from serv.service import api_request
from datetime import datetime
from user.forms.mixin import DetailSityMixin


class IndexView(DetailSityMixin, ProcessFormView, TemplateView):
    template_name = "solar/index.html"



    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        article = api_request(
            'sancta/article/{0}.json'.format('12_vazhnyh_dnyay_so_dnya_rozhdeniya')
        )
        article = json.loads(article)
        context['article'] = article
        context['url'] = 'home'
        return context




    def form_valid(self, form):

        self.form_save_session_values(form)

        d, m, y = map(int, form.cleaned_data['date'].split('.'))
        h, mm = map(int, form.cleaned_data['time'].split(':'))
        if int(form.cleaned_data['is_russian']):
            city_id = int(form.cleaned_data['city_id'])
        else:
            city_id = int(form.cleaned_data['detail_city'])

        year = datetime.today().year
        b_dt = datetime(y, m, d, h, mm)



        return HttpResponseRedirect(
            reverse('solar_open', kwargs={
                'date': b_dt.strftime('%Y%m%d%H%M'),
                'city_id':city_id,
                'year': year,
            })
        )
