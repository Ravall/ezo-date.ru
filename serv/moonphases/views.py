import datetime
from serv.views import CityLiveMixin, ServiceMixin
from moonbirthday.service import get_geo_by_cityid
from user.service.moon import get_moonday_info
from user.forms.form import CityLiveForm
from django.views.generic.edit import ProcessFormView, FormMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from user.service.city import get_city_by_id


class MoonPhasesService(CityLiveMixin, ServiceMixin):
    service = 'moonphases'

    def get_context_data(self, **kwargs):
        context = super(MoonPhasesService, self).get_context_data(**kwargs)
        city, city_id = self.get_city()
        self.geo = get_geo_by_cityid(city_id)
        context.update({
            'now': self.now,
            'moon_info': get_moonday_info(self.now, self.geo),
            'city': city,
            'geo': self.geo
        })
        return context


class IndexView(MoonPhasesService):
    url = 'moonphases_home'
    template_name = "moonphases/index.html"


class MoonPhasesArticles(MoonPhasesService):
    url = 'moonphases_articles'
    template_name = "moonphases/articles.html"   

    def get_context(self, **kwargs):
        return {
            'articles': self.api_get_by_tags('moon_phases')
        }


class Article(MoonPhasesService):
    url = 'moonphases_articles'
    template_name = "moonphases/article.html"

    def get_context(self, **kwargs):
        return {
            'article':self.api_get_article(kwargs['artname'])
        }


class MonthView(MoonPhasesService):
    url = 'moonphases_month'
    template_name = "moonphases/month.html"

    def get_context_data(self, **kwargs):
        context = super(MonthView, self).get_context_data(**kwargs)
        first_day = self.now.replace(day=1, hour=0, second=0, minute=0, microsecond=0)
        day = first_day
        mooon_month = []
        while day.month == self.now.month:
            info = get_moonday_info(day, context['geo'], False)
            mooon_month.append(info)
            day = info['periods']['this_day'][1] + datetime.timedelta(seconds=1)
        context['mooon_month'] = mooon_month
        return context


class MoonPhasesForm(ProcessFormView, FormMixin, MoonPhasesService):
    url = 'moonphases_form'
    template_name = "moonphases/form.html"
    form_class = CityLiveForm

    def form_valid(self, form):
        self.request.session['moonphases_city_id'] = self.request.POST['city_live_1']
        return HttpResponseRedirect(reverse_lazy('moonphases_form_result'))


class MoonPhasesFormResult(MonthView):
    url = 'moonphases_form'
    template_name = "moonphases/month.html"
    city_id = False

    def get(self, request, *args, **kwargs):
        self.city_id = request.session.pop('moonphases_city_id', False)
        if not self.city_id:
            return HttpResponseRedirect(reverse_lazy('moonphases_form'))
        return super(MoonPhasesFormResult, self).get(request, *args, **kwargs)

    def get_city(self):
        if not self.city_id:
            return super(MoonPhasesFormResult, self).get_city()
        return [get_city_by_id(self.city_id).name_ru, self.city_id]













