# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView
from serv.service import api_request


class MoonbirthdayNum(TemplateView):
    template_name = "moonbirthday/num.html"


    def get(self, request, digit):
        num = int(digit)
        if num < 1 or num > 30:
            raise Http404
        content = api_request(
            'sancta/article/{0}_lunnyy_den_rozhdeniya.json'.format(num)
        )
        content = json.loads(content)

        return self.render_to_response({
            'num': num,
            'content': content,
            'url': 'all'
        })