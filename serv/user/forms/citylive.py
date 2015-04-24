# -*- coding: utf-8 -*-
from django import forms
from user.forms.basecity import BaseCityForm


class CityLiveForm(BaseCityForm):

    city_error_text = 'Выберете город проживания'
    city_placeholder_text = 'Введите город, где вы живете'








