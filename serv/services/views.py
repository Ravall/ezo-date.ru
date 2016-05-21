# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class ListView(TemplateView):
    template_name = "services/list.html"
