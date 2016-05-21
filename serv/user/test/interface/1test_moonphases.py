# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.test import TestCase
from django.conf import settings
from user.test import data_provider
from user.service import moon
from django.test import Client


class MoonphasesCase(TestCase):
    fixtures = [
        os.path.abspath(
            os.path.join(settings.PATH, '../', 'files', 'fixtures', 'city_for_tests.json')
        )
    ]


    def test_open(self):
        c = Client()
        response = c.get('/moonphases/')
        self.assertEquals(200, response.status_code)


        response = c.get(
            '/moonphases/',
            {
                'date': 198311242300,
                'city_id': 524305
            }
        )
        self.assertEquals(200, response.status_code)
