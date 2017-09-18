# -*- coding: utf-8 -*-
import json
import calendar
from django.views.generic.edit import ProcessFormView, FormMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from user.service import biorythms as bio_service
from snct_date.date import today, day_maps, yyyy_mm_dd, date_shift, num_days_in_month
from serv.views import ServiceMixin, LoginRequiredMixin
from user.forms.form import BirthdayForm
from bio_calendar import MyHtmlCalendar


class BiorythmsService(ServiceMixin):
    service = 'biorythms'


class IndexView(BiorythmsService):
    template_name = 'biorythms/index.html'
    url = 'bio_home'

    def get_context(self, **kwargs):
        return {
            'content': self.api_get_article('biorythms_about')
        }


class ArticlesView(BiorythmsService):
    template_name = 'biorythms/articles.html'
    url = 'biorythms_articles'

    def get_context(self, **kwargs):
        return {
            'articles': self.api_get_by_tags('biorythms'),
            'articles_emo': self.api_get_by_tags('emo_biorhythm'),
            'articles_mind': self.api_get_by_tags('mind_biorhythm'),
            'articles_fiz': self.api_get_by_tags('fiz_biorhythm')
        }


class ArticleView(BiorythmsService):
    template_name = 'biorythms/article.html'
    url  = 'biorythms_articles'

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article(kwargs['artname'])
        }


class BioContext(BiorythmsService):
    current_date = today()
    today = yyyy_mm_dd(today())



    def get_context(self, **kwargs):
        date = self.get_date()
        if not date:
            return {}
        date_tuple = date.split('.')
        bio_context = bio_service.get_bio_context(date_tuple, self.current_date)

        bio_context['data'] = json.dumps(bio_context['data'])
        bio_context.update({'date_map':
            {k: yyyy_mm_dd(v) for k,v in day_maps(self.current_date).items()}
        })

        myCal = MyHtmlCalendar(calendar.MONDAY, 'ru_RU.UTF-8')
        myCal.current_date = self.current_date
        bio_context.update({
            'today': self.today,
            'calendar': myCal.formatmonth(self.current_date[2], self.current_date[1])
        })
        return bio_context


class BioMy(LoginRequiredMixin, BioContext):
    template_name = 'biorythms/biorythm.html'
    url = 'bio_my'


class AjaxGetData(LoginRequiredMixin, BioContext):
    template_name = 'biorythms/bio_info.html'

    def get(self, request, *args, **kwargs):
        self.current_date = map(int, self.request.GET['day'].split('-')[::-1])
        return super(AjaxGetData, self).get(request, *args, **kwargs)


class BioFormView(BioContext, ProcessFormView, FormMixin, BiorythmsService):
    template_name = 'biorythms/form.html'
    url = 'form'
    form_class = BirthdayForm

    def get_date(self):
        return self.request.session.pop('bio_date', '')

    def get_initial(self):
        return {
            'date': self.request.session.get('bio_date', '')
        }

    def form_valid(self, form):
        self.request.session['bio_date'] = form.cleaned_data['date']
        return HttpResponseRedirect(
            reverse_lazy(
                'bio_form'
            )
        )
