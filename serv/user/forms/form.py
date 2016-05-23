# -*- coding: utf-8 -*-
import re
from django import forms
from moonbirthday.forms.validator import validator_city
from django_mobile import get_flavour
from user.forms.elements.widgets import DateBornMobile, TimeBornMobile
from user.forms.elements.fields import DateElement, TimeElement, CityElement
#from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from collections import OrderedDict
from django.contrib.auth.models import User


default_choices = [('0', '----------')]


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class BirthdayForm(forms.Form):
    '''
    Форма с датой рождения
    '''
    date = DateElement()


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
    '''
    расширенная форма даты рождения. Добавлено время
    '''
    time = TimeElement()


class CityLiveForm(forms.Form):
    city_live = CityElement(label="Город проживания")


class FullBirthdayForm(BirthdayTimeForm):
    '''
    полная информация о рождении
    '''
    city = CityElement()





#class BaseCityForm(forms.Form):
#   city_error_text = 'Выберете город'
#   city_placeholder_text = 'Введите город'
#
#    city=forms.CharField(
#        label="Город рождения",
#        validators=[validator_city],
#        widget=forms.TextInput(
#            attrs={'placeholder': 'введите город'}
#        ),
#    )
#    city_id=forms.CharField(
#        widget=forms.HiddenInput(), required=False
#    )
#    is_russian= forms.CharField(
#        widget=forms.HiddenInput(), required=False
#    )
#    country = ChoiceFieldNoValidation(label="Страна")
#    region  = ChoiceFieldNoValidation(label="Регион")
#    detail_city = ChoiceFieldNoValidation(label="Город")



#    def clean_detail_city(self):
#        form_data = self.cleaned_data
#        if form_data['is_russian'] == '0' and form_data['detail_city'] == '0':
#            raise forms.ValidationError(self.city_error_text)
#        return form_data['detail_city']


#class FullBirthdayForm(BirthdayTimeForm, BaseCityForm):
#    '''
#    полная форма рождения.
#    '''
#    pass


#class CityLiveForm(BaseCityForm):
#    city_error_text = 'Выберете город проживания'
#    city_placeholder_text = 'Введите город, где вы живете'



class CheckMobileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.flavour = kwargs.pop('flavour', get_flavour())
        super(CheckMobileForm, self).__init__(*args, **kwargs)
        if self.flavour == 'mobile':
            self.fields['date'].widget = DateBornMobile()
            self.fields['time'].widget = TimeBornMobile()



#class RegForm(CheckMobileForm, BaseCityForm):
#    username = forms.CharField(label='Логин')
#    error_messages = {
#        'password_mismatch': "Пароли не совпадают",
#        'username_doesnt_unic': "Пользователь с таким логином уже зарегистирован на сайте",
#        'email_doesnt_unic': "Пользователь с таким email уже зарегистирован на сайте"
#    }
#    date = DateElement()
#    time = TimeElement(initial='10:00')
#    email = forms.EmailField(label="E-mail")
#    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#    password2 = forms.CharField(label="Подвердите пароль", widget=forms.PasswordInput)
#
#    def __init__(self, *args, **kwargs):
#        super(RegForm, self).__init__(*args, **kwargs)
#        self.fields = OrderedDict(
#            (k, RegForm.base_fields[k])
#            for k in [
#                'username', 'email', 'date', 'time', 'password1', 'password2',
#                'city', 'city_id', 'is_russian', 'country', 'region', 'detail_city'
#            ]
#        )
#
#    def clean_username(self):
#        '''
#        username должен быть уникальным
#        '''
#        username = self.cleaned_data.get("username")
#        objs = User.objects.filter(username=username).count()
#        if objs>0:
#            raise forms.ValidationError(
#                self.error_messages['username_doesnt_unic'],
#                code='username_doesnt_unic',
#            )
#        return username
#
#
#    def clean_email(self):
#        '''
#        email должен быть уникальным
#        '''
#        email = self.cleaned_data.get("email")
#        objs = User.objects.filter(email=email).count()
#        if objs>0:
#            raise forms.ValidationError(
#                self.error_messages['email_doesnt_unic'],
#                code='email_doesnt_unic',
#            )
#        return email
#
#
#    def clean_password2(self):
#        '''
#        Пароли должны совпадать
#        '''
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("pa.ssword2")
#        if password1 and password2 and password1 != password2:
#            raise forms.ValidationError(
#                self.error_messages['password_mismatch'],
#                code='password_mismatch',
#            )
#        return password2

