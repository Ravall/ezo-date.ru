# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class V2(TemplateView):
    template_name = "frontend/v2.html"