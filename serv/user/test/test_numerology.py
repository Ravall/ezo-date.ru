# -*- coding: utf-8 -*-
from django.test import TestCase
from user.test import data_provider
from user.service import numerology

class BirthdaNumCase(TestCase):

    def provider_moondays():
        return (
            #  Я
            ('3.11.1983', 8),
            ('03.11.1983', 8),
            # Данис со своим редким ДР
            ('26.13.1981', 4),

        )


    @data_provider(provider_moondays)
    def test_moonbirthday(self, date, num):
        self.assertEquals(numerology.get_birthday_num(date), num)