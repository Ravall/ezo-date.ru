# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from moonbirthday.models import SxgeoCities
from moonbirthday.views.ajax import AjaxTemplateMixin
from collections import OrderedDict


class Ajax(AjaxTemplateMixin, TemplateView):

    def get_context_data(self, **kwargs):
        region_id = self.request.GET.get('region_id')
        return OrderedDict(
            [(x.id, x.name_ru) for x in SxgeoCities.objects.order_by('name_ru').filter(region_id=region_id)]
        )


