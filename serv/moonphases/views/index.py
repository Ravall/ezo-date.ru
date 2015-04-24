# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView, FormMixin
from django.http import HttpResponseRedirect
from serv.service import api_request
from datetime import datetime
from user.forms.citymixin import CityMixin
from moonbirthday.service import get_geo_by_cityid, _to_local
from moonphases.service import get_moonday_info


class IndexView(CityMixin, ProcessFormView, TemplateView):
    template_name = "moonphases/index.html"



    def get_context_data(self, **kwargs):
        city, city_id = self.get_city()
        geo = get_geo_by_cityid(city_id)

        moon_info =  get_moonday_info(datetime.now(), geo)

        context = super(IndexView, self).get_context_data(**kwargs)
        article = api_request(
            'sancta/article/{0}.json'.format('12_vazhnyh_dnyay_so_dnya_rozhdeniya')
        )
        article = json.loads(article)
        context['article'] = article
        context['url'] = 'home'
        context['info'] = moon_info
        context['city'] = city
        return context




    def form_valid(self, form):
        self.form_save_session_values(form)
        return HttpResponseRedirect(
            reverse('moonphases_home', kwargs={})
        )
