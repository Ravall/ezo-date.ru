# -*- coding: utf-8 -*-
'''
Тут хранятся миксины ко вьюшкам
'''
import json
from serv.service import api_request
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from user.forms.form import BirthdayForm, FullBirthdayForm, CityLiveForm
from django.http import HttpResponse


class HttpResponse303(HttpResponseRedirect):
    status_code = 303


class AjaxTemplateMixin(object):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.is_ajax():
            return HttpResponse(json.dumps(context))
        else:
            return HttpResponse(context)


class ApiRequestMixin(TemplateView):
    '''
    Миксин с запросами к API
    '''

    
    def api_get_article(self, article_name):
        '''
        получение статьи по названию
        '''
        content_raw = api_request(
            'sancta/article/{0}.json'.format(article_name)
        )
        if content_raw:
            content = json.loads(content_raw)
        else:
            content = ''
        return content


    def api_get_by_tags(self, tag):
        '''
        получение статей по тегу
        '''
        content_raw = api_request(
            'sancta/article/tag/{0}.json'.format(tag)
        )
        if content_raw:
            content = json.loads(content_raw)
        else:
            content = ''
        return content


class SessionMixin(FormMixin):
    '''
    общий миксин, с методами сохранения в сессии данных формы
    '''
    key = 'born'


    def get_value(self, key, default=None):
        return self.request.session.get(
            '{1}_{0}'.format(self.key, key),
            default
        )

    
    def save_to_session(self, form):
        for key in form.cleaned_data.keys():
            self.save_value(key, key, form)

    
    def save_value(self, key_form, key_session, form):

        self.request.session[
            '{0}_{1}'.format(key_session, self.key)
        ] = form.cleaned_data[key_form]



class BirthDayFormMixin(SessionMixin):
    form_class = BirthdayForm


    def get_initial(self):
        return {'date': self.get_value('date')}



class FullBirthDayFormMixin(BirthDayFormMixin):
    form_class = FullBirthdayForm

    def get_initial(self):
        return {
            'date': self.get_value('date'),
            'time': self.get_value('time'),
            'city': self.get_value('city'),
        }
   

class CityFormMixin(SessionMixin):
    form_class = CityLiveForm

    def get_initial(self):
        return {
            'city_live': self.get_value('city_live', self.get_value('city'))
        }


