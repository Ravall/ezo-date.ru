# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView
from serv.service import api_request


class List(TemplateView):
    template_name = "solar/12.html"

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        context['articles'] = json.loads(
            api_request(
                'sancta/article/tag/{0}.json'.format('solar12')
            )
        )
        context['url'] = 'all'
        return context


