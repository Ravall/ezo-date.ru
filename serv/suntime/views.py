# -*- coding: utf-8 -*-
from serv.views import CityLiveMixin, ServiceMixin
from user.service.sun import get_sun_info
from moonbirthday.service import get_geo_by_cityid
from django.views.generic.edit import ProcessFormView, FormMixin
from user.forms.form import CityLiveForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from user.service.city import get_city_by_id


class SuntimeSerivce(CityLiveMixin, ServiceMixin):
    service = 'suntime'

    def get_context_data(self, **kwargs):
        context = super(SuntimeSerivce, self).get_context_data(**kwargs)
        city, city_id = self.get_city()
        self.geo = get_geo_by_cityid(city_id)
        context.update({
            'now': self.now,
            'sun_info': get_sun_info(self.now, self.geo),
            'city': city,
            'geo': self.geo
        })
        return context


class IndexView(SuntimeSerivce):
    template_name = 'suntime/index.html'
    url = 'suntime_home'


class ArticlesView(SuntimeSerivce):
    template_name = 'suntime/articles.html'
    url = 'suntime_articles'

    def get_context(self, **kwargs):
        return {
            'articles': self.api_get_by_tags('suntime')
        }


class ArticleView(SuntimeSerivce):
    template_name = 'suntime/article.html'
    url = 'suntime_articles'

    def get_context(self, **kwargs):
        return {
            'article': self.api_get_article(kwargs['artname'])
        }


class ArticlesFormView(ProcessFormView, FormMixin, SuntimeSerivce):
    url = 'suntime_form'
    template_name = "suntime/form.html"
    form_class = CityLiveForm

    def form_valid(self, form):
        self.request.session['suntime_city_id'] = self.request.POST['city_live_1']
        return HttpResponseRedirect(reverse_lazy('suntime_form_result'))


class ArticlesFormResultView(IndexView):
    url = 'suntime_form'
    template_name = 'suntime/index.html'
    city_id = False

    def get(self, request, *args, **kwargs):
        self.city_id = request.session.pop('suntime_city_id', False)
        if not self.city_id:
            return HttpResponseRedirect(reverse_lazy('suntime_form'))
        return super(ArticlesFormResultView, self).get(request, *args, **kwargs)

    def get_city(self):
        if not self.city_id:
            return super(ArticlesFormResultView, self).get_city()
        return [get_city_by_id(self.city_id).name_ru, self.city_id]


