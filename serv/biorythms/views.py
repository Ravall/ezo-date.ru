# -*- coding: utf-8 -*-
import json
from datetime import  date
from serv.service import api_request
from django.views.generic.edit import ProcessFormView
from django.views.generic import TemplateView
from serv.views import (
    ApiRequestMixin, BirthDayFormMixin, SessionMixin,
    HttpResponse303, AjaxTemplateMixin
)
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from user.service import biorythms as bio_service
from snct_date.date import (
    today, day_maps, yyyy_mm_dd, date_shift, num_days_in_month
)
import calendar


calendar.month_name = calendar._localized_month("%OB")


class MyHtmlCalendar(calendar.LocaleHTMLCalendar):
    today = date.today()


    def formatday(self, day, weekday):
        css = [self.cssclasses[weekday]]
        if (
            day == self.today.day and
            self.today.month == self.month and
            self.today.year == self.year
        ):
            css.append('today')

        if self.current_date == [day, self.month, self.year]:
            css.append('selected')

        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            return (
                '<td class="%s">'
                '<a class="get_bio_data" day="%s" href="#">%d</a>'
                '</td>'
            ) % (
                ' '.join(css),
                yyyy_mm_dd((day, self.month, self.year)),
                day
            )


    def formatmonthname(self, theyear, themonth, withyear=True):
        with calendar.TimeEncoding(self.locale) as encoding:
            s = calendar.month_name[themonth]
            if encoding is not None:
                s = s.decode(encoding)
            if withyear and theyear != self.today.year:
                s = '%s, %s' % (s, theyear)
            prev_month_day = yyyy_mm_dd(
                date_shift(1, themonth, theyear, -1)
            )
            next_month_day = yyyy_mm_dd(
                date_shift(
                    num_days_in_month(themonth,theyear),
                    themonth, theyear, 1
                )
            )
            return (
                '<tr><th colspan="7" class="month">'
                '<a href="#" day="%s" class="get_bio_data">&larr;</a> '
                '%s'
                ' <a href="#" day="%s" class="get_bio_data">&rarr;</a>'
                '</th></tr>'
            )% (prev_month_day, s, next_month_day)


    def formatmonth(self, theyear=today.year, themonth=today.month, withyear=True):
        self.year = theyear
        self.month = themonth
        return super(MyHtmlCalendar, self).formatmonth(theyear, themonth, withyear)


class BiorythmsMixin(TemplateView):
    url = ''


    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'biorythms')
        kwargs.setdefault('url', self.url)
        return super(BiorythmsMixin, self).get_context_data(**kwargs)


class IndexView(ApiRequestMixin, BiorythmsMixin):
    template_name = 'biorythms/index.html'
    url = 'bio_home'


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'content': self.api_get_article('biorythms_about')
        })
        return context


class BioFormView(BirthDayFormMixin, ProcessFormView, BiorythmsMixin, SessionMixin):
    template_name = 'biorythms/form.html'
    url = 'form'


    def form_valid(self, form):
        self.save_value('date', 'date', form)
        return HttpResponseRedirect(
            reverse_lazy(
                'bio_result'
            )
        )


class BioResult(BiorythmsMixin, SessionMixin):
    template_name = 'biorythms/biorythm.html'
    url = 'bio_result'
    current_date = today()
    today = yyyy_mm_dd(today())


    def get(self, request, *args, **kwargs):
        return super(BioResult, self).get(request, *args, **kwargs) \
            if self.get_value('date') \
            else HttpResponse303(reverse_lazy(
                'bio_form'
            ))


    def get_context_data(self, **kwargs):
        context = super(BioResult, self).get_context_data(**kwargs)
        date_bd = self.get_value('date').split('.')
        bio_context = bio_service.get_bio_context(
            self.get_value('date').split('.'),
            self.current_date
        )
        bio_context['data'] = json.dumps(bio_context['data'])
        context.update(bio_context)
        context.update({'date_map':
            {k: yyyy_mm_dd(v) for k,v in day_maps(self.current_date).items()}
        })
        myCal = MyHtmlCalendar(calendar.MONDAY, 'ru_RU.UTF-8')
        myCal.current_date = self.current_date
        context.update({
            'today':self.today,
            'calendar':myCal.formatmonth(self.current_date[2], self.current_date[1])
        })
        return context


class AjaxGetData(BioResult):
    template_name = 'biorythms/bio_info.html'


    def get_context_data(self, **kwargs):
        self.current_date = map(int, self.request.GET['day'].split('-')[::-1])
        context = super(AjaxGetData, self).get_context_data(**kwargs)
        return context


