# -*- coding: utf-8 -*-
from serv.views import ApiRequestMixin, BirthDayFormMixin, SessionMixin, HttpResponse303
from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from user.service.numerology import get_birthday_num
from django.http import Http404



class NumerologyMixin(TemplateView):
    url = ''
    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'numerology')
        kwargs.setdefault('url', self.url)
        return super(NumerologyMixin, self).get_context_data(**kwargs)


class IndexView(ApiRequestMixin, NumerologyMixin):
    template_name = 'numerology/index.html'
    url  = 'num_home'


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'article': self.api_get_article('chislo_rozhdeniya_raschet')
        })
        return context


class NumerologyFormView(BirthDayFormMixin, ProcessFormView, NumerologyMixin, SessionMixin):
    template_name = 'numerology/form.html'
    url = 'form'

    def form_valid(self, form):
        result = get_birthday_num(form.cleaned_data['date'])
        self.save_value('date', 'date', form)
        return HttpResponseRedirect(
            reverse_lazy(
                'num_birthday',kwargs = {'digit':result}
            )
        )


class AllNumsView(NumerologyMixin):
    template_name = 'numerology/all.html'
    url = 'all'

    def get_context_data(self, **kwargs):
        context = super(AllNumsView, self).get_context_data(**kwargs)
        context.update({
            'all_nums': (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22),
        })
        return context


class NumView(ApiRequestMixin, NumerologyMixin, SessionMixin):
    template_name = 'numerology/num.html'

    def get(self, request, *args, **kwargs):
        digit = int(kwargs['digit'])
        if not( (digit > 0 and digit < 10) or digit in (11, 22) ):
            raise Http404
        date = self.get_value('date')
        if date and digit == get_birthday_num(date):
            self.url = 'my_num'
        return super(NumView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NumView, self).get_context_data(**kwargs)
        context.update({
            'all_nums': (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22),
            'num': kwargs['digit'],
            'article': self.api_get_article(
                'chislo_rozhdeniya_{0}'.format(kwargs['digit'])
            )
        })
        return context


class NumerologyResult(RedirectView, SessionMixin):

    def get(self, request, *args, **kwargs):
        date = self.get_value('date')
        self.url = reverse_lazy(
            'num_birthday', kwargs = {'digit':get_birthday_num(date)}
        ) if date else reverse_lazy('num_form')
        return HttpResponse303(self.url)

