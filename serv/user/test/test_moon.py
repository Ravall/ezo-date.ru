# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.test import TestCase
from django.conf import settings
from user.test import data_provider
from user.service import moon

class MoonBirthdayCase(TestCase):
    fixtures = [
        os.path.abspath(
            os.path.join(settings.PATH, '../', 'files', 'fixtures', 'city_for_tests.json')
        )
    ]
    def provider_moondays():
        return (
            #  Я
            (
                {
                    'lat':'53.62462',
                    'long':'55.95015',
                    'timezone':'Asia/Yekaterinburg'
                },
                datetime(1983, 11, 3, 23, 0),
                28
            ),
            # Данис со своим редким ДР
            (
                {
                    'lat':'53.62462',
                    'long':'55.95015',
                    'timezone':'Asia/Yekaterinburg'
                },
                datetime(1981, 12, 26, 13, 0),
                30
            ),
            # Мурманск
            (
                {
                    'lat':'68.97917',
                    'long':'33.09251',
                    'timezone':'Europe/Moscow'
                },
                datetime(1983, 11, 3, 23, 0),
                29
            ),
        )


    @data_provider(provider_moondays)
    def test_moonbirthday(self, geo, date, moon_day):
        self.assertEquals(moon.get_moon_day_by_geo(geo, date), moon_day)


    def provider_moondays_bycity():
        return (
            #  Я
            (487495, datetime(1983, 11, 3, 23, 0), 28),
            # Данис со своим редким ДР
            (487495, datetime(1981, 12, 26, 13, 0), 30),
            # Мурманск
            (524305, datetime(1983, 11, 3, 23, 0), 29),
        )


    @data_provider(provider_moondays_bycity)
    def test_moonbirthday_bycity(self, city, date, moon_day):
        _moon_day = moon.get_moon_day_by_cityid(city, date)
        self.assertEquals(_moon_day, moon_day)



    def provider_moonday_info():
        return (
            (
                {
                    'lat':'53.62462',
                    'long':'55.95015',
                    'timezone':'Asia/Yekaterinburg'
                },
                datetime(1981, 12, 26, 13, 1),
                {
                    'moon_day': 30,
                }
            ),
            (
                {
                    'lat':'68.97917',
                    'long':'33.09251',
                    'timezone':'Europe/Moscow'
                },#198311242300
                datetime(1983, 11, 24, 13, 1),
                {
                    'previous_rising': 'AlwaysUp',
                    'next_setting': 'AlwaysUp'
                }
            )

        )

    @data_provider(provider_moonday_info)
    def test_get_moonday_info(self, geo, dt, info_r):
        info = moon.get_moonday_info(dt, geo)
        for k, v in info_r.items():
            self.assertEquals(info_r[k], info[k])



    def test_moon_periods(self):
        # москва
        geo = {
            'lat': '55.75222',
            'long': '37.61556',
            'timezone': 'Europe/Moscow'
        }
        dt = datetime(2015, 05, 8, 12, 0)
        info = moon.get_moonday_info(dt, geo)
        self.assertEquals(
            info['periods']['new'][0].replace(second=0, microsecond=0),
            datetime(2015, 4, 18, 21, 56)
        )
        self.assertEquals(
            info['periods']['new'][1].replace(second=0, microsecond=0),
            datetime(2015, 4, 19, 5, 45)
        )
        self.assertEquals(
            info['periods']['waxing'][0].replace(second=0, microsecond=0),
            datetime(2015, 4, 19, 5, 45)
        )
        self.assertEquals(
            info['periods']['waxing'][1].replace(second=0, microsecond=0),
            datetime(2015, 5, 3, 19, 19)
        )
        self.assertEquals(
            info['periods']['full'][0].replace(second=0, microsecond=0),
            datetime(2015, 5, 3, 19, 19)
        )
        self.assertEquals(
            info['periods']['full'][1].replace(second=0, microsecond=0),
            datetime(2015, 5, 4, 20, 27)
        )
        self.assertEquals(
            info['periods']['waning'][0].replace(second=0, microsecond=0),
            datetime(2015, 5, 4, 20, 27)
        )
        self.assertEquals(
            info['periods']['waning'][1].replace(second=0, microsecond=0),
            datetime(2015, 5, 18, 7, 13)
        )

    def test_what_period(self):
        # москва
        geo = {
            'lat': '55.75222',
            'long': '37.61556',
            'timezone': 'Europe/Moscow'
        }
        dt = datetime(2015, 05, 8, 12, 0)
        info = moon.get_moonday_info(dt, geo)
        self.assertEquals(
            moon.what_period(info['periods'], datetime(2015, 5, 8, 12, 0)),
            'waning'
        )
        self.assertEquals(
            moon.what_period(info['periods'], datetime(2015, 5, 4, 0, 0)),
            'full'
        )





