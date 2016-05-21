# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.edit import FormMixin
from moonbirthday.forms.form import FullDateAndPlaceBird
from django_mobile import get_flavour
from moonbirthday.service import get_default_city, get_city_by_id
#from user.forms.form import CityLiveForm



#class CityMixin(FormMixin):
#    key = 'live'
#    form_class = CityLiveForm
#
#    def get_city(self, city_id=False):
#        if city_id:
#            city, city_id = get_city_by_id(city_id)
#        if not city_id  or not city:
#            city = self.get_from_session('city', False)
#            city_id = self.get_from_session('city_id', False)
#        if not city_id or not city:
#            city, city_id = get_default_city(self.request.META['REMOTE_ADDR'])
#        return city, city_id
#
#
#    def get_from_session(self, key, default=None):
#        return self.request.session.get('{1}_{0}'.format(self.key, key), default)
#
#
#    def get_initial(self):
#        city, city_id = self.get_city()
#        return {
#            'city': city,
#            'city_id': city_id,
#            'is_russian': self.get_from_session('is_russian', 1),
#            'country': self.get_from_session('country'),
#            'region': self.get_from_session('region'),
#            'detail_city': self.get_from_session('detail_city'),
#        }
#
#    def save_in_session(self, key_form, key_session, form):
#        self.request.session[
#            '{0}_{1}'.format(key_session, self.key)
#        ] = form.cleaned_data[key_form]
#
#
#
#   def form_save_session_values(self, form):
#        for key in ['city_id', 'city', 'is_russian']:
#            self.save_in_session(key, key, form)
#        if form.cleaned_data['is_russian'] == '0':
#            for key in ['country', 'region', 'detail_city']:
#                self.save_in_session(key, key, form)





#class DetailSityMixin(CityMixin):
#    key = 'born'
#    form_class = FullDateAndPlaceBird
#
#
#    # add the request to the kwargs
#    def get_form_kwargs(self):
#        kwargs = super(DetailSityMixin, self).get_form_kwargs()
#        kwargs.update({'flavour': get_flavour()})
#        return kwargs
#
#
#    def get_initial(self):
#        initial = super(DetailSityMixin, self).get_initial()
#        initial['date'] = self.get_from_session('birthday')
#        initial['time'] = self.get_from_session('time')
#        return initial
#
#
#    def form_save_session_values(self, form):
#        initial = super(DetailSityMixin, self).form_save_session_values(form)
#        self.save_in_session('date', 'birthday', form)
#        self.save_in_session('time', 'time', form)







