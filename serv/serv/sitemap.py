# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class ReversItem(object):
    def __init__(self, route_name, args=[]):
        self.route_name = route_name
        self.args = args

    def get_absolute_url(self):
        return reverse(self.route_name, args=self.args)


class DigitSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            ReversItem('num_birthday', [digit])
            for digit in range(1,10) + [11,22]
        ]

class MoonbirthdayNums(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            ReversItem('moon_birthday_num', [digit])
            for digit in range(1, 31)
        ]


class SolarDays(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            ReversItem('solar_day', [digit])
            for digit in range(1, 13)
        ]


class SimplePage(Sitemap):
    changefreq = "weekly"
    priority = 1

    def items(self):
        return [
            ReversItem(route_name)
            for route_name in [
                'num_home', 'all_nums',
                'bio_home',
                'moon_birthday_home', 'moon_birthday_all_nums',
                'solar_home', 'solar_12_days', 'moonphases_home'
            ]
        ]


sitemaps = {
    'digit': DigitSitemap,
    'moonbirthdayNums': MoonbirthdayNums,
    'solar': SolarDays,
    'pages': SimplePage
}