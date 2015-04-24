# -*- coding: utf-8 -*-
import re
from datetime import datetime
from django import forms
from django.forms import widgets as django_widgets
from moonbirthday.forms.validator import validator_date, validator_time, validator_city
from moonbirthday.models import SxgeoCountry
from moonbirthday.service import get_moon_bithday
from django_mobile import get_flavour


default_choices = [('0', '----------')]


class DateInput(django_widgets.DateInput):
    input_type = 'date'


class TimeInput(django_widgets.TimeInput):
    input_type = 'time'


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class FullDateAndPlaceBird(forms.Form):


    date = forms.CharField(
        label="Дата",
        widget=django_widgets.TextInput(
            attrs={
                'placeholder': 'введите дату рождения',
            },
        ),
        validators=[validator_date],
        error_messages = {
            'required': "введите дату. Пример: 03.11.1983",
        }
    )
    time = forms.CharField(
        label="Время",
        widget=django_widgets.TextInput(
            attrs={'placeholder': 'введите время рождения'}
        ),
        validators=[validator_time],
        error_messages = {
            'required': "введите время. Пример: 23:01",
        }
    )
    city = forms.CharField(
        label="Город",
        validators=[validator_city],
        widget=forms.TextInput(
            attrs={'placeholder': 'введите город рождения'}
        ),
    )
    city_id = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    is_russian = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    country = ChoiceFieldNoValidation(label="Страна")
    region = ChoiceFieldNoValidation(label="Регион")
    detail_city = ChoiceFieldNoValidation(label="Город")

    def __init__(self, *args, **kwargs):
        self.flavour = kwargs.pop('flavour', get_flavour())
        super(FullDateAndPlaceBird, self).__init__(*args, **kwargs)
        if self.flavour == 'mobile':
            self.fields['date'].widget = DateInput(attrs={
                'placeholder': 'введите дату рождения',
            })
            self.fields['time'].widget = TimeInput(attrs={
                'placeholder': 'введите время рождения',
            })


    def clean_detail_city(self):
        form_data = self.cleaned_data
        if form_data['is_russian'] == '0' and form_data['detail_city'] == '0':
            raise forms.ValidationError('Выберете город в котором вы родились')
        return form_data['detail_city']


    def clean_date(self):
        form_data = self.cleaned_data
        if re.match('[0-9]{2,4}\-[0-9]{1,2}\-[0-9]{1,2}',form_data['date']):
            clean = '.'.join(form_data['date'].split('-')[::-1])
        else:
            clean = form_data['date']
        return clean


    def process(self):
        d, m, y = map(int, self.cleaned_data['date'].split('.'))
        h, mm = map(int, self.cleaned_data['time'].split(':'))
        if int(self.cleaned_data['is_russian']):
            city_id = int(self.cleaned_data['city_id'])
        else:
            city_id = int(self.cleaned_data['detail_city'])
        moon_bithday = get_moon_bithday(datetime(y, m, d, h, mm), city_id)
        return moon_bithday

