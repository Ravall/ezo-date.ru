from django.contrib.auth.models import User
from django.db import models
from moonbirthday.models import SxgeoCities


class EzoUser(models.Model):
    user = models.OneToOneField(User)
    city_born = models.IntegerField()
    city_live = models.IntegerField(null=True, blank=True)
    date_born = models.DateField()
    time_born = models.TimeField()