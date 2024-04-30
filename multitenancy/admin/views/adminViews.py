import json
from django.urls.base import reverse, reverse_lazy
import sweetify

# import environ
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

# import time
from django.forms.models import modelform_factory

from tenant_users.tenants.utils import get_tenant_model, get_tenant_domain_model
from multitenancy.admin.decorators import allowed_users
from multitenancy.admin.models import Admin, Settings
from multitenancy.order.models import Order
from multitenancy.profiles.models import Profile
from tenant_users.tenants.models import InactiveError, ExistsError
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from helpdesk.models import Ticket
from multitenancy.admin.filters import CustomerFilter


from multitenancy.subscriptions.models import (
    Plan,
    ProductFeature,
    ProductType,
    Subscription,
)
from multitenancy.teams.models import SimpleTeam, Team
from account.mixins import LoginRequiredMixin


from multitenancy.users.models import Customer, TenantUser
from multitenancy.apps.models import Tenant
from .baseViews import (
    AdminListView,
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    AdminView,
    AdminDetailView,
)

# env = environ.Env()


class AdminIndexView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        app_configs = Admin.app_configs
        # app_configs = sorted(app_configs, key=lambda x: x.menu_order)
        groups = {}
        context["apps"] = app_configs

        # for app_config in app_configs:
        #     group = groups.get(app_config.group, [])
        #     group.append(app_config)
        #     groups[app_config.group] = group
        #     context['apps'] = group

        context["subscriptions"] = (
            get_tenant_model()
            .objects.all()
            .exclude(schema_name="public")
            .exclude(is_template=True)
        )
        context["users"] = TenantUser.objects.all()
        context["revenue"] = Tenant.total_revenue()
        ProductType.objects.create_defaults()
        context["staff"] = Profile.objects.filter()
        active_date = []
        active_count = []
        inactive_count = []
        for date in Subscription.get_active_inactive_subscriptions_data():
            active_date.append(date[0])
            active_count.append(date[1])
            inactive_count.append(date[2])

        context["active_date"] = json.dumps(active_date)
        context["active_count"] = json.dumps(active_count)
        context["inactive_count"] = json.dumps(inactive_count)

        context["customers"] = Customer.objects.filter().exclude(email="AnonymousUser")
        context["users"] = TenantUser.objects.all()
        context["active_tickets"] = Ticket.objects.select_related("queue").exclude(
            status__in=[Ticket.CLOSED_STATUS, Ticket.RESOLVED_STATUS],
        )
        return context


class TeamsIndexView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/teamIndex.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["simple_teams"] = SimpleTeam.objects.all()
        context["teams"] = Team.objects.all()
        return context
