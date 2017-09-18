# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError
from snct_date.date import is_date_correct
from user.service.city import is_city_exists, get_city_by_id


def validator_date(value):
    value = value.replace('_','')
    if not (
        re.match('^\d{1,2}\.\d{1,2}\.(\d{2}|\d{4})$',value)
        and is_date_correct(*value.split('.'))
    ) and  not (
        re.match('^(\d{2}|\d{4})\-\d{1,2}\-\d{1,2}$',value)
        and is_date_correct(*value.split('-')[::-1])
    ):
        raise ValidationError('некорректная дата. Введите дату в формате дд.мм.гггг')


def validator_time(value):
    reg = re.match('^([0-9]{1,2})\:([0-9]{2})(\:[0-9]{2})?$',value)
    if not reg:
        raise ValidationError('некорректное время. Введите время в формате чч:мм')
    h, m = map(int, reg.groups()[0:2])
    if not (h>=0 and h<24 and m>=0 and m<60):
        raise ValidationError('некорректное время')


def validator_city(value):
    value = re.sub('\(.*\)', '', value).strip()
    if not is_city_exists(value):
        raise ValidationError(
            'Город вашего рождения не найден. '
            'Укажите ближайший крупный город или воспользуйтесь подробным поиском .'
        )


def validator_city_field(value):
    '''
    консистентность поля CityElement(forms.MultiValueField)
    проверяем нет ли расхождений между id города в скрытом поле
    и названием города в форме. 
    '''
    text_error = 'Произошла ошибка в поиске города (Форма не консистентна). Попробуйте еще раз'
    city_name, city_id = value.split('%%')
    city_name = re.sub('\(.*\)', '', city_name).strip()
    try:
        result = get_city_by_id(city_id)
    except:
        raise ValidationError(text_error)
    if not result.name_ru == city_name:
        ValidationError(text_error)

