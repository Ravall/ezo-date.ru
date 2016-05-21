from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models import EzoUser

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EzoUserInline(admin.StackedInline):
    model = EzoUser
    can_delete = False
    verbose_name_plural = 'ezouser'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (EzoUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)