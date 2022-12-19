from django.contrib import admin
from multitenancy.users.models import TenantUser

@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'type')
