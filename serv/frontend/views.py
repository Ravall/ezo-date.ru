# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from numerology.models import BirthdayForm
from datetime import datetime, timedelta, date
from django.shortcuts import redirect


def index(request):

    if request.method == 'POST':
        birthday_form = BirthdayForm(request.POST)
        if birthday_form.is_valid():
            birthday = datetime.strptime(
                birthday_form.cleaned_data['date'], '%d.%m.%Y'
            ).strftime('%Y-%m-%d')
            request.session['birthday'] = birthday_form.cleaned_data['date']
    else:
        birthday_form = BirthdayForm(initial={'date':request.session.get('birthday')})


    return render_to_response(
        'frontend/index.html',
        {
            'form': birthday_form,
        },
        context_instance=RequestContext(request)
    )
