# -*- coding: utf-8 -*-
import os
from django.views.generic.base import TemplateView
from django.views.generic.edit import ProcessFormView, FormMixin
from django.http import HttpResponseRedirect
from frontend.models import SubscribeForm
from django.contrib import messages
from django.conf import settings


class V2(FormMixin, ProcessFormView, TemplateView):
    template_name = "frontend/v2.html"
    form_class = SubscribeForm
    success_url = '/v2'


    def form_valid(self, form):
        file_to  = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'subscibe.txt'))
        handle1 = open(file_to, 'a')
        handle1.write('email: {0} \n'.format(form.cleaned_data['email']))
        handle1.close()
        messages.add_message(self.request, messages.INFO, 'Вы успешно подписаны')
        return HttpResponseRedirect(self.get_success_url())
