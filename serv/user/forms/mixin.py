from django.views.generic.edit import FormMixin
from moonbirthday.forms.form import FullDateAndPlaceBird
from django_mobile import get_flavour
from moonbirthday.service import get_default_city


class DetailSityMixin(FormMixin):
    form_class = FullDateAndPlaceBird


    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DetailSityMixin, self).get_form_kwargs()
        kwargs.update({'flavour': get_flavour()})
        return kwargs


    def get_initial(self):
        city = self.request.session.get('city', False)
        city_id = self.request.session.get('city_id', False)
        if not city_id or not city:
            city, city_id = get_default_city(self.request.META['REMOTE_ADDR'])
        return {
            'date':self.request.session.get('birthday'),
            'time': self.request.session.get('time'),
            'city': city,
            'city_id': city_id,
            'is_russian': self.request.session.get('is_russian', 1),
            'country': self.request.session.get('country'),
            'region': self.request.session.get('region'),
            'detail_city': self.request.session.get('detail_city'),
        }


    def form_save_session_values(self, form):
        self.request.session['birthday'] = form.cleaned_data['date']
        def save_in_session(key, form):
            self.request.session[key] = form.cleaned_data[key]

        for key in ['time', 'city_id', 'city', 'is_russian']:
            save_in_session(key, form)
        if form.cleaned_data['is_russian'] == '0':
            for key in ['country', 'region', 'detail_city']:
                save_in_session(key, form)
