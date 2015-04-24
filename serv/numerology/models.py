# -*- coding: utf-8 -*-
import re
from snct_date.date import is_date_correct
from django.db import models
from django import forms
from django.forms import widgets as django_widgets
from django.core.exceptions import ValidationError
import time
from django_mobile import get_flavour

class DateInput(django_widgets.DateInput):
    input_type = 'text'


def validator_date(value):
    if not (
        re.match('[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4}',value)
        and is_date_correct(*value.split('.'))
    ) and  not (
        re.match('[0-9]{2,4}\-[0-9]{1,2}\-[0-9]{1,2}',value)
        and is_date_correct(*value.split('-')[::-1])
    ):
        raise ValidationError('введите в формате дд.мм.гггг')




class BirthdayForm(forms.Form):
    date = forms.CharField(
        widget=DateInput(
            attrs={'placeholder': 'введите дату рождения'}
        ),
        validators=[validator_date],
        error_messages = {
            'required': "введите дату. Пример: 03.11.1983",
        }
    )

    def clean_date(self):
        form_data = self.cleaned_data
        if re.match('[0-9]{2,4}\-[0-9]{1,2}\-[0-9]{1,2}',form_data['date']):
            clean = '.'.join(form_data['date'].split('-')[::-1])
        else:
            clean = form_data['date']
        return clean


def get_birthday_num(data):
    def num(data):
        while True:
            data = reduce(lambda res, x: res+int(x), list(str(data)), 0)
            if data < 10 or data in (11, 22):
                break
        return data
    return num(''.join(data.split('.')))


