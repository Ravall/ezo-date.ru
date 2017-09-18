# -*- coding: utf-8 -*-
from serv.views import AjaxTemplateMixin
from django.views.generic import TemplateView
from user.service.city import city_like_as
from registration.backends.model_activation.views import RegistrationView as RegView
from registration.backends.model_activation.views import ActivationView as ActView
from user.forms.form import FullBirthdayForm, FamilyForm
from django.views.generic.edit import ProcessFormView
from serv.views import ProfileMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.db import transaction


class AjaxCity(AjaxTemplateMixin, TemplateView):
    """Автодополнение городов в
    форме для сохранения своего города рождения"""

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        return {
            'query': query,
            'suggestions': city_like_as(query)
        }


class ActivationView(ActView):

    def get_success_url(self, user):
        return ('user_profile', (), {})

    @transaction.atomic
    def activate(self, *args, **kwargs):
        activated_user = super(ActivationView, self).activate(*args, **kwargs)
        if not activated_user:
            return False
        activated_user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(self.request, activated_user)
        return activated_user


class RegistrationView(RegView):
    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'registration')
        return super(RegistrationView, self).get_context_data(**kwargs)


class ProfileForm(FamilyForm, FullBirthdayForm):

    def save(self, request, profile):
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.first_name = self.cleaned_data['first_name']
        profile.city_id = self.get_city_id(request)
        profile.born_date = self.get_bd()
        profile.sex = self.cleaned_data['sex']
        profile.new_last_name = self.cleaned_data['new_last_name'] if self.cleaned_data['sex'] == 'f' else None
        profile.city_live_id = self.get_city_id(request, 'city_live_1')
        profile.is_emigrated = self.cleaned_data['is_emigrated']
        profile.city_live_id = self.get_city_id(request, 'city_live_1') if self.cleaned_data['is_emigrated'] else None
        profile.user.save()
        profile.save()



class ProfileFormMixin(TemplateView):
    url = ''

    def get_context_data(self, **kwargs):
        kwargs.setdefault('service', 'user_profile')
        kwargs.setdefault('url', self.url)
        return super(ProfileFormMixin, self).get_context_data(**kwargs)


class ProfileView(ProcessFormView, ProfileFormMixin, ProfileMixin):
    form_class = ProfileForm
    template_name = 'user/profile.html'
    url = 'user_profile'

    def form_valid(self, form):
        form.save(self.request, self.profile)
        return HttpResponseRedirect(reverse_lazy('user_profile'))


class PasswordChangeView(FormMixin, ProcessFormView, ProfileFormMixin):
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    url = 'auth_settings'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Пароль успешно изменен')
        return HttpResponseRedirect(reverse_lazy('auth_settings'))


