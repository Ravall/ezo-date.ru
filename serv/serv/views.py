# -*- coding: utf-8 -*-
'''
Тут хранятся миксины ко вьюшкам
'''
import json
import datetime
from serv.service import api_request
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import HttpResponse
from user.models import EzoUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


class ProfileMixin(FormMixin):
    '''
    общий миксин, с методами сохранения
    '''
    profile = False

    def get_initial(self):
        self.profile, is_created = EzoUser.objects.select_related().get_or_create(
            user_id=self.request.user.id
        )
        return dict(
            [(key, self.get_value(key)) for key in self.form_class.declared_fields.keys()]
        )

    def get_value(self, key):
        fn = getattr(self.profile, "get_{}".format(key), None)
        if callable(fn):
            return fn()
        return getattr(self.profile, key)


class ServiceMixin(ApiRequestMixin):
    url = ''
    profile = False
    service = ''

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', self.service)
        kwargs.setdefault('url', self.url)
        context = super(ServiceMixin, self).get_context_data(**kwargs)
        context.update(self.get_context(**kwargs))
        return context


class LoginRequiredMixin(object):
    def get(self, request, *args, **kwargs):
        try:
            self.profile = EzoUser.objects.select_related().get(pk=self.request.user.id)
        except EzoUser.DoesNotExist:
            messages.add_message(self.request, messages.WARNING, 'Требуется заполнить профиль')
            return HttpResponseRedirect(reverse_lazy('user_profile'))
        return super(LoginRequiredMixin, self).get(request, *args, **kwargs)

    def get_date(self):
        return self.profile.get_date()

    def get_bd(self):
        return self.profile.born_date

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class CityLiveMixin(object):
    now = datetime.datetime.now()
    geo = None

    def get_city(self):
        try:
            profile = EzoUser.objects.select_related().get(pk=self.request.user.id)
            city_name, city_id = profile.get_city_live()
            if not city_id:
                raise Exception()
        except Exception:
            city_id = settings.MOONBIRTHDAY['default_city_id']
            city_name = settings.MOONBIRTHDAY['default_city']
        return [city_name, city_id]




