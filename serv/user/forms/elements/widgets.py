# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from user.service.city import get_default_city


class ElementBorn(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        field = super(ElementBorn, self).render(name, value, attrs)
        return mark_safe(render_to_string(
            self.template_name,
            {
                'field':field,
                'attrs':attrs
            }
        ))


class DateBorn(ElementBorn):
    template_name = 'user/form/dateborn_widget.html'


class TimeBorn(ElementBorn):
    template_name = 'user/form/timeborn_widget.html'


class DateBornMobile(DateBorn):
     input_type = 'date'


class TimeBornMobile(DateBorn):
     input_type = 'time'


class CityElementWidget(ElementBorn):
    template_name = 'user/form/city_widget.html'



class CityWidget(forms.MultiWidget):
    widgets = [
        CityElementWidget(),
        forms.HiddenInput()
    ]
    
    def __init__(self, *args, **kwargs):
        return super(CityWidget, self).__init__(self.widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return value.split('%%')
        return [None, None]

