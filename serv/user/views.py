# -*- coding: utf-8 -*-
from serv.views import AjaxTemplateMixin
from django.views.generic import TemplateView
from user.service.city import city_like_as


class AjaxCity(AjaxTemplateMixin, TemplateView):
	'''
	Автодополнение городов в форме для сохранения своего города рождения
	'''


	def get_context_data(self, **kwargs):
		query = self.request.GET.get('query')
		return {
			'query': query, 
			'suggestions': city_like_as(query)
		}