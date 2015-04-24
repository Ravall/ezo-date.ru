# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError
from snct_date.date import is_date_correct
from moonbirthday.service import is_city_exists


def validator_date(value):
    if not (
        re.match('[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4}',value)
        and is_date_correct(*value.split('.'))
    ) and  not (
        re.match('[0-9]{2,4}\-[0-9]{1,2}\-[0-9]{1,2}',value)
        and is_date_correct(*value.split('-')[::-1])
    ):
        raise ValidationError('некорректная дата. Введите дату в формате дд.мм.гггг')


def validator_time(value):
    if not re.match('[0-9]{1,2}\:[0-9]{2}',value):
        raise ValidationError('некорректное время. Введите время в формате чч:мм')
    h,m = map(int, value.split(':'))
    if not (h>=0 and h<24 and m>=0 and m<60):
        raise ValidationError('некорректное время')


def validator_city(value):
    if not is_city_exists(value):
        raise ValidationError(
            'Город вашего рождения не найден. '
            'Укажите ближайший крупный город или воспользуйтесь подробным поиском .'
        )

