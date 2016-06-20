# -*- coding: utf-8 -*-
import json
from pysitemap import SiteMap
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from serv.service import api_request


class mySiteMap(SiteMap):
    def __init__(self, *args, **kwargs):
        current_site = Site.objects.get_current()
        self.base_url = current_site.domain
        self.changefreq = kwargs.get('changefreq','weekly')
        return super(mySiteMap, self).__init__(*args, **kwargs)

    def add(self, url, *args, **kwargs):
        kwargs['changefreq'] = kwargs.get('changefreq',self.changefreq)
        return super(mySiteMap, self).add(
            loc='http://{0}{1}'.format(self.base_url, url), 
            *args, **kwargs
        )



def api_get_by_tags(tag):
    content_raw = api_request(
        'sancta/article/tag/{0}.json'.format(tag)
    )
    if content_raw:
        api_articles = json.loads(content_raw)
    else:
        api_articles = []
    return [art['name'] for art in api_articles]


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        sm = mySiteMap()

        # страницы, где появляются новые статьи
        for url in [
            'all_nums', 'moonbirthday_nums', 'solar_12',
             'moonphases_articles', 'suntime_articles', 'bio_articles'
        ]:
            sm.add(reverse(url), priority=1.0)
        # просто страницы
        for url in [
            'num_form', 'num_home', 
            'bio_home', 'bio_form', 
            'moonbirthday_home', 'moonbirthday_form',
            'solar_home', 'solar_form',
            'moonphases_home', 'moonphases_month', 'moonphases_city',
            'suntime_home', 'suntime_city'
        ]:
            sm.add(reverse(url))
        # статьи с нумерологией
        for num in (range(1, 10) + [11, 22]):
            sm.add(reverse('num_birthday', args=[num]))
        # статьи лунного дня рождения
        for num in range(1, 31):
            sm.add(reverse('moonbirthday_one_num', args=[num]))
        # статьи открытие соляра
        for num in range(1, 13):
            sm.add(reverse('solar_day', args=[num]))
        # статьи фазы луны
        for article_name in api_get_by_tags('moon_phases'):
            sm.add(reverse('moonphases_article', args=[article_name]))
        # статьи истинного полдня
        for article_name in api_get_by_tags('suntime'):
            sm.add(reverse('suntime_article', args=[article_name]))
        # статьи биоритмы
        for article_name in api_get_by_tags('biorythms'):
            sm.add(reverse('bio_article', args=[article_name]))
            

        out = open('{0}/xml/sitemap.xml'.format(settings.MEDIA_ROOT), 'w')
        out.write(sm.to_string())
        out.close()
