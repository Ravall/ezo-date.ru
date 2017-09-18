# -*- coding: utf-8 -*-
from datetime import datetime
from django.views.generic.edit import ProcessFormView, FormMixin
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from serv.views import ServiceMixin, LoginRequiredMixin, ProfileMixin
from user.forms.form import FullBirthdayForm
from user.service.moon import get_moon_bithday


class MoonBirthdayService(ServiceMixin):
    service = 'moonbirthday'


class IndexView(MoonBirthdayService):
    url = 'moonbirthday_home'
    template_name = "moonbirthday/index.html"

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article('lunnyy_den_rozhdeniya')
        }


class NumsView(MoonBirthdayService):
    url = 'moonbirthday_nums'
    template_name = "moonbirthday/nums.html"

    def get_context(self, **kwargs):
        return {
            'articles': self.api_get_by_tags('moon_birthday')
        }


class OneNumView(MoonBirthdayService, ProfileMixin):
    """
    Просмотр статьи о конкретном лунном дне 
    """
    template_name = "moonbirthday/oneday.html"
    url = 'moonbirthday_nums'

    def get(self, request, *args, **kwargs):
        num = int(kwargs['nday'])
        if num < 1 or num > 30:
            raise Http404
        return super(OneNumView, self).get(request, *args, **kwargs)

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article('{0}_lunnyy_den_rozhdeniya'.format(kwargs['nday'])),
            'nums': range(1, 31),
            'num': kwargs['nday']
        }


class FormView(ProcessFormView, FormMixin, MoonBirthdayService):
    url = 'form'
    template_name = "moonbirthday/form.html"
    form_class = FullBirthdayForm

    def form_valid(self, form):
        b_dt = '{0} {1}'.format(form.cleaned_data['date'], form.cleaned_data['time'])
        born_date = datetime.strptime(b_dt, '%d.%m.%Y %H:%M')
        return HttpResponseRedirect(reverse_lazy(
            'moonbirthday_one_num',
            kwargs={'nday':get_moon_bithday(born_date, self.request.POST['city_1'])}
        ))


class MyDayView(LoginRequiredMixin, MoonBirthdayService):
    url = 'my'
    template_name = "moonbirthday/oneday.html"

    def get_context(self, **kwargs):
        num = get_moon_bithday(self.profile.born_date, self.profile.city_id)
        return {
            'num': num,
            'article': self.api_get_article('{0}_lunnyy_den_rozhdeniya'.format(num))
        }
