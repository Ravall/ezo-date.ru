# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from moonbirthday.models import SxgeoRegions
from moonbirthday.views.ajax import AjaxTemplateMixin
from collections import OrderedDict


class Ajax(AjaxTemplateMixin, TemplateView):

    def get_context_data(self, **kwargs):
        country_id = self.request.GET.get('country_id')
        return OrderedDict(
            [(x.id, x.name_ru) for x in SxgeoRegions.objects.order_by('name_ru').filter(country=country_id)]
        )


