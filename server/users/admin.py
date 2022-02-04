from django.contrib import admin

# Register your models here.
from users.models import UserModel


class UsersAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(UserModel,UsersAdmin)