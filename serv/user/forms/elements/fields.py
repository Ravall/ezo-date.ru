# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import widgets as django_widgets
from validator import validator_date, validator_time, validator_city, validator_city_field
from user.forms.elements.widgets import DateBorn, TimeBorn, CityWidget


class DateElement(forms.CharField):
    widget=DateBorn(attrs={'placeholder': 'пример 03.11.1983'})
    default_error_messages = {
        'required': "введите дату. Пример: 03.11.1983"
    }


    def __init__(self, *args, **kwargs):
        super(DateElement, self).__init__(*args, **kwargs)
        self.label = 'Дата рождения'
        self.validators.append(validator_date)


class TimeElement(forms.CharField):
    widget=TimeBorn(attrs={'placeholder': 'время рождения'})
    default_error_messages = {
        'required': "введите дату. Пример: 23:00"
    }

    def __init__(self, *args, **kwargs):
        super(TimeElement, self).__init__(*args, **kwargs)
        self.label = 'Время рождения'
        self.validators.append(validator_time)


class CityField(forms.CharField):
    
    def __init__(self, *args, **kwargs):
        super(CityField, self).__init__(*args, **kwargs)
        self.validators.append(validator_city)


class CityElement(forms.MultiValueField):
    widget = CityWidget()
    default_error_messages = {
        'required': "Введите город в котором вы родились"
    }
    fields = [CityField(), forms.CharField()]

    def __init__(self, *args, **kwargs):
        super(CityElement, self).__init__(self.fields, *args, **kwargs)
        self.validators.append(validator_city_field)
        self.label = kwargs.get('label','Город рождения')
        
    
    def compress(self, data_list):
        return '{0}%%{1}'.format(data_list[0], data_list[1])

    
        
