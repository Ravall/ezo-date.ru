# -*- coding: utf-8 -*-
from django.views.generic.edit import ProcessFormView, FormMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from serv.views import ServiceMixin, LoginRequiredMixin
from user.forms.form import BirthdayForm
from user.service.numerology import get_birthday_num


class NumerologyService(ServiceMixin):
    service = 'numerology'


class IndexView(NumerologyService):
    template_name = 'numerology/index.html'
    url = 'num_home'

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article('chislo_rozhdeniya_raschet')
        }


class NumerologyFormView(ProcessFormView, FormMixin, NumerologyService):
    template_name = 'numerology/form.html'
    form_class = BirthdayForm
    url = 'form'

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse_lazy(
                'num_birthday',
                kwargs={'digit': get_birthday_num(form.cleaned_data['date'])}
            )
        )


class AllNumsView(NumerologyService):
    template_name = 'numerology/all.html'
    url = 'num_all'

    def get_context(self, **kwargs):
        return {
            'all_nums': range(1, 10) + [11, 22],
        }


class NumView(NumerologyService):
    template_name = 'numerology/num.html'
    url = 'num_all'

    def get(self, request, *args, **kwargs):
        digit = int(kwargs['digit'])
        if digit not in (range(1, 10)+[11, 22]):
            raise Http404
        return super(NumView, self).get(request, *args, **kwargs)

    def get_context(self, **kwargs):
        return {
            'all_nums':  range(1, 10) + [11, 22],
            'num': kwargs['digit'],
            'article': self.api_get_article(
                'chislo_rozhdeniya_{0}'.format(kwargs['digit'])
            )
        }


class NumerologyMy(LoginRequiredMixin, NumerologyService):
    template_name = 'numerology/num.html'
    url = 'num_my'

    def get_context(self, **kwargs):
        date = self.profile.get_date()
        digit = get_birthday_num(date)

        return {
            'num': digit,
            'article': self.api_get_article(
                'chislo_rozhdeniya_{0}'.format(digit)
            )
        }






