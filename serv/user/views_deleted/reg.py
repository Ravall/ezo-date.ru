from datetime import datetime
from django.conf import settings
#from registration.models import RegistrationProfile
#from registration import signals
#from registration.views import RegistrationView
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django_mobile import get_flavour
from django.shortcuts import redirect
from user.models import EzoUser
#from user.forms.form import RegForm
#from user.forms.mixin import DetailSityMixin



class RegView():#RegistrationView, DetailSityMixin):
 #   form_class = RegForm
    success_url='registration_complete'
    SEND_ACTIVATION_EMAIL = True


    def get_form_kwargs(self):
        kwargs = super(RegView, self).get_form_kwargs()
        kwargs.update({'flavour': get_flavour()})
        return kwargs


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return super(RegView, self).dispatch(request, args, kwargs)


    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)


    def register(self, request, form):
        self.form_save_session_values(form)
        user = User.objects.create_user(
            form.cleaned_data.get('username'),
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password1'),
            last_login=datetime.today()
        )
        city_id = form.cleaned_data.get('city_id') \
            if form.cleaned_data.get('is_russian') == '1' \
            else form.cleaned_data.get('detail_city')

        new_user_instance = EzoUser(
            user=user,
            city_born = city_id,
            date_born = datetime.strptime(form.cleaned_data.get('date'), '%d.%m.%Y'),
            time_born = datetime.strptime(form.cleaned_data.get('time'), '%H:%M').time()
        ).save()

        new_user = RegistrationProfile.objects.create_inactive_user(
            Site.objects.get_current(),
            user,
            self.SEND_ACTIVATION_EMAIL,
        )
        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=request
        )

