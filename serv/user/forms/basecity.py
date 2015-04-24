# -*- coding: utf-8 -*-
from django import forms
from moonbirthday.forms.validator import validator_city


default_choices = [('0', '----------')]


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass


class BaseCityForm(forms.Form):

    city_error_text = 'Выберете город'
    city_placeholder_text = 'Введите город'

    city = forms.CharField(
        label="Город",
        validators=[validator_city],
        widget=forms.TextInput(
            attrs={'placeholder': 'введите город'}
        ),
    )
    city_id = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    is_russian = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    country = ChoiceFieldNoValidation(label="Страна")
    region  = ChoiceFieldNoValidation(label="Регион")
    detail_city = ChoiceFieldNoValidation(label="Город")

    def __init__(self, *args, **kwargs):
        super(BaseCityForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget = forms.TextInput(
            attrs={'placeholder': self.city_placeholder_text}
        )


    def clean_detail_city(self):
        form_data = self.cleaned_data
        if form_data['is_russian'] == '0' and form_data['detail_city'] == '0':
            raise forms.ValidationError(self.city_error_text)
        return form_data['detail_city']






