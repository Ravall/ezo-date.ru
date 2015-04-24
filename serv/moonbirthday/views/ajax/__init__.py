from django.http import HttpResponse
from django.utils import simplejson


class AjaxTemplateMixin(object):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.is_ajax():
            return HttpResponse(simplejson.dumps(context))
        else:
            return HttpResponse(context)
