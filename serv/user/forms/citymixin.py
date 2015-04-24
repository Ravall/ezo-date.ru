from django.views.generic.edit import FormMixin
from user.forms.citylive import CityLiveForm
from moonbirthday.service import get_default_city


class CityMixin(FormMixin):
    form_class = CityLiveForm

    def get_city(self):
        city = self.request.session.get('city_live', False)
        city_id = self.request.session.get('city_id_live', False)
        if not city_id or not city:
            city, city_id = get_default_city(self.request.META['REMOTE_ADDR'])
        return city, city_id

    def get_initial(self):
        city, city_id = self.get_city()
        return {
            'city': city,
            'city_id': city_id,
            'is_russian': self.request.session.get('is_russian_live', 1),
            'country': self.request.session.get('country_live'),
            'region': self.request.session.get('region_live'),
            'detail_city': self.request.session.get('detail_city_live'),
        }


    def form_save_session_values(self, form):
        def save_in_session(key, form):
            self.request.session['{0}_live'.format(key)] = form.cleaned_data[key]

        for key in ['city_id', 'city', 'is_russian']:
            save_in_session(key, form)
        if form.cleaned_data['is_russian'] == '0':
            for key in ['country', 'region', 'detail_city']:
                save_in_session(key, form)
