from multitenancy.admin.models import Admin, register_admin
from .models import Tenant,Domain


@register_admin
class TenantAdmin(Admin):
    model = Tenant
    menu_label = 'Templates'
    menu_order = 200
    menu_icon = 'fas fa-copy'
    list_display = ['id', 'name', 'type', 'is_template', 'plan', 'description', 'subscription', 'trail_duration', 'on_trial', 'created', 'modified']    

@register_admin
class DomainAdmin(Admin):
    model = Domain
    menu_label = 'My Model'
    menu_order = 200
    menu_icon = 'site'
    list_display = ['id', 'name', 'type', 'is_template', 'plan', 'description', 'subscription', 'trail_duration', 'on_trial', 'created', 'modified']    

