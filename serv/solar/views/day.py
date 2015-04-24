# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView
from serv.service import api_request


class Show(TemplateView):
    template_name = "solar/day.html"

    def get(self, request, nday):
        num = int(nday)
        if num < 1 or num > 12:
            raise Http404
        content = api_request(
            'sancta/article/day_{0}.json'.format(num)
        )
        content = json.loads(content)

        return self.render_to_response({
            'num': num,
            'content': content,
            'url': 'all'
        })