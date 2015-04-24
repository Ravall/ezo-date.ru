# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView
from serv.service import api_request


class MoonbirthdayAllNums(TemplateView):
    template_name = "moonbirthday/all_nums.html"

    def get_context_data(self, **kwargs):
        context = super(MoonbirthdayAllNums, self).get_context_data(**kwargs)
        context['articles'] = json.loads(
            api_request(
                'sancta/article/tag/{0}.json'.format('moon_birthday')
            )
        )
        context['url'] = 'all'
        return context


