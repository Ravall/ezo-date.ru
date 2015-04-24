# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from moonbirthday.service import city_like_as
from moonbirthday.views.ajax import AjaxTemplateMixin


class Ajax(AjaxTemplateMixin, TemplateView):


    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        return {'query': query, 'suggestions': city_like_as(query)}


