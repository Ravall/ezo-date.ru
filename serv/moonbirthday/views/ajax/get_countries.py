# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from moonbirthday.models import SxgeoCountry
from moonbirthday.views.ajax import AjaxTemplateMixin
from collections import OrderedDict


class Ajax(AjaxTemplateMixin, TemplateView):

    def get_context_data(self, **kwargs):
        return OrderedDict(
            [(x.iso, x.name_ru) for x in SxgeoCountry.objects.order_by('name_ru')]
        )


