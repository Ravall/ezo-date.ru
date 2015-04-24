# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.views.generic import TemplateView
from serv.service import api_request
from solar.service import get_solar_time


class OpenView(TemplateView):
    template_name = "solar/open.html"


    def get(self, request, city_id, date, year):
        b_dt = datetime.strptime(date,'%Y%m%d%H%M')
        time = get_solar_time(b_dt, city_id, int(year))
        diff = datetime.today() - time
        day = (diff.days + 1)

        if (day >0 and day <13):
            content = api_request(
                'sancta/article/day_{0}.json'.format(day)
            )
            content = json.loads(content)
        else:
            content = False

        return self.render_to_response({
            'day': day,
            'time': time,
            'city_id': city_id,
            'year': year,
            'b_dt': date,
            'article': content,
            'url': 'all'
        })