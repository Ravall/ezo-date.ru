from django.conf import settings
from django.contrib.sites.models import Site


def debug(context):
    return {'DEBUG': settings.DEBUG}


def site_name(context):
    current_site = Site.objects.get_current()
    
    return {
        'SITE_URL':current_site.domain
    }