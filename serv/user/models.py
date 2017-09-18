from django.contrib.auth.models import User
from django.db import models


class SxGeoCity(models.Model):
    id = models.IntegerField(primary_key=True)
    region_id = models.IntegerField()
    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    lon = models.DecimalField(max_digits=10, decimal_places=5)
    okato = models.CharField(max_length=20)

    class Meta:
       managed = False
       db_table = 'sxgeo_cities'


class EzoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(SxGeoCity, null=True, blank=True, related_name='city')
    city_live = models.ForeignKey(SxGeoCity, null=True, blank=True, related_name='city_live')
    born_date = models.DateTimeField(null=True, blank=True)
    new_last_name = models.CharField(max_length=256, null=True, blank=True)
    sex = models.CharField(max_length=1, null=True, blank=True)
    is_emigrated = models.BooleanField(default=False)

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name


    def get_city(self):
        return [self.city.name_ru, self.city_id] if self.city else ['','']

    def get_city_live(self):
        return [self.city_live.name_ru, self.city_live_id] if self.city_live else ['','']

    def get_date(self):

        return self.born_date.strftime('%d.%m.%Y') if self.born_date else ''

    def get_time(self):
        return self.born_date.strftime('%H:%M') if self.born_date else ''


