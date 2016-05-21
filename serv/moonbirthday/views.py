# -*- coding: utf-8 -*-
from datetime import datetime
from user.service.moon import get_moon_bithday
from django.views.generic import TemplateView, RedirectView
from serv.views import ApiRequestMixin, SessionMixin, FullBirthDayFormMixin
from django.views.generic.edit import ProcessFormView
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy



class MoonBirthdayMixin(TemplateView):
    url = ''


    def get_moonbirthday(self):
        if not self.get_value('city'):
            return False
        city, city_id = self.get_value('city').split('%%')
        b_dt = '{0} {1}'.format(self.get_value('date'), self.get_value('time'))
        b_dt = datetime.strptime(b_dt, '%d.%m.%Y %H:%M')
        return get_moon_bithday(b_dt, city_id)


    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'moonbirthday')
        kwargs.setdefault('url', self.url)
        return super(MoonBirthdayMixin, self).get_context_data(**kwargs)


class IndexView(ApiRequestMixin, MoonBirthdayMixin):
    url = 'moonbirthday_home'
    template_name = "moonbirthday/index.html"


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'article': self.api_get_article('lunnyy_den_rozhdeniya')
        })
        return context


class NumsView(ApiRequestMixin, MoonBirthdayMixin):
    url = 'moonbirthday_nums'
    template_name = "moonbirthday/nums.html"


    def get_context_data(self, **kwargs):
        context = super(NumsView, self).get_context_data(**kwargs)
        context.update({
            'articles': self.api_get_by_tags('moon_birthday')
        })
        return context



class OneNumView(ApiRequestMixin, MoonBirthdayMixin, SessionMixin):
    '''
    Просмотр статьи о конкретном лунном дне 
    '''
    template_name = "moonbirthday/oneday.html"
    url = 'moonbirthday_nums'

    def get(self, request, *args, **kwargs):
        num = int(kwargs['nday'])
        if num < 1 or num > 30:
            raise Http404
        return super(OneNumView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.get_moonbirthday() == int(kwargs['nday']):
            self.url = 'my'
        context = super(OneNumView, self).get_context_data(**kwargs)
        context['article'] = self.api_get_article('{0}_lunnyy_den_rozhdeniya'.format(context['nday']))
        context['nums'] = range(1,31)
        context['num'] = context['nday']
        
        return context


class FormView(FullBirthDayFormMixin, ProcessFormView, MoonBirthdayMixin, SessionMixin):
    url = 'form'
    template_name = "moonbirthday/form.html"

    def form_valid(self, form):
        self.save_to_session(form)
        return HttpResponseRedirect(reverse_lazy('moonbirthday_my_day'))


class MyDayView(ApiRequestMixin, MoonBirthdayMixin, SessionMixin):
    url = 'my'
    template_name = "moonbirthday/oneday.html"

    def get(self, request, *args, **kwargs):
        if not (
            self.get_value('date') and self.get_value('time') and self.get_value('city')
        ):
            return HttpResponseRedirect(reverse_lazy('moonbirthday_form'))
        return super(MyDayView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MyDayView, self).get_context_data(**kwargs)

        num = self.get_moonbirthday()
        context['article'] = self.api_get_article('{0}_lunnyy_den_rozhdeniya'.format(num))
        context['nums'] = range(1, 31)
        context['num'] = num
        return context