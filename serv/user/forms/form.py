# -*- coding: utf-8 -*-
import re
from django import forms
from datetime import datetime
from django_mobile import get_flavour
from user.forms.elements.widgets import DateBornMobile, TimeBornMobile
from user.forms.elements import fields

default_choices = [('0', '----------')]


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class BirthdayForm(forms.Form):
    date = fields.DateElement()

    def clean_date(self):
        form_data = self.cleaned_data
        date = form_data['date'].replace('_', '')
        if re.match('[0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}',date):
            clean = '.'.join(date.split('-')[::-1])
        else:
            clean = date
        date_ar = clean.split('.')
        y = int(date_ar[2])
        if y < 100:
            y += 2000 if y<10 else 1900
        date_ar[2] = str(y)
        clean = '.'.join(date_ar)
        return clean


class BirthdayTimeForm(BirthdayForm):
    time = fields.TimeElement()

    def clean_time(self):
        return re.match('^([0-9]{1,2}\:[0-9]{2})(\:[0-9]{2})?', self.cleaned_data['time']).groups()[0]


class CityLiveForm(forms.Form):
    city_live = fields.CityElement(label="Город проживания")


class FullBirthdayForm(BirthdayTimeForm):
    city = fields.CityElement()

    def get_city_id(self, request, id='city_1'):
        return request.POST[id]

    def get_bd(self):
        b_dt = '{0} {1}'.format(self.cleaned_data['date'], self.cleaned_data['time'])
        return datetime.strptime(b_dt, '%d.%m.%Y %H:%M')


class FamilyForm(forms.Form):
    first_name = fields.NameElement()
    last_name = fields.SurnameElement()
    sex = fields.SexElement()
    new_last_name = fields.NewSurnameElement(required=False)
    is_emigrated = forms.BooleanField(label='Я живу в другом городе', required=False)
    city_live = fields.CityElement(label='Город', required=False)


class CheckMobileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.flavour = kwargs.pop('flavour', get_flavour())
        super(CheckMobileForm, self).__init__(*args, **kwargs)
        if self.flavour == 'mobile':
            self.fields['date'].widget = DateBornMobile()
            self.fields['time'].widget = TimeBornMobile()



