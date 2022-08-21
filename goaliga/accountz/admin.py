from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','first_name','last_name','is_active','last_login',)
    list_display_links=('email','first_name','last_name',)
    readonly_fields=('last_login','date_joined',)

    filter_horizontal= ()
    list_filter= ()
    fieldsets= ()
    ordering = ('email',)

admin.site.register(Account,AccountAdmin)