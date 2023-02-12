import os
from multitenancy.apps.forms import TenantForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import permissions
from django.urls.base import reverse, reverse_lazy
from django.http import HttpResponseRedirect
import sweetify
from tenant_users.tenants.models import InactiveError, ExistsError
from tenant_users.tenants.utils import (get_tenant_model,
                                        get_tenant_domain_model)
from django.conf import settings
from django.shortcuts import redirect, render
from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import(
    AdminListView,
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    AdminView,
    AdminDetailView,
    CustomerTemplateView,
    CustomerView
    )
from .filters import TenantFilter
from multitenancy.subscriptions.models import Plan, Subscription
from .models import Tenant
from .serializers import TenantSerializer


class TemplateListView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/apps/template_list.html"

class CreateTemplateView(LoginRequiredMixin, AdminCreateView):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('template_list')
    template_name = 'multitenancy/apps/create_template.html'

    def post(self, request, is_staff=True, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data["name"]
            tenant_slug = form.cleaned_data["slug"]
            type = form.cleaned_data['type']
            user = request.user

            if not user.is_active:
                raise InactiveError("Inactive user passed to provision tenant")
            tenant_domain = '{}.{}'.format(
                tenant_slug,  settings.TENANT_USERS_DOMAIN)
            DomainModel = get_tenant_domain_model()
            if DomainModel.objects.filter(domain=tenant_domain).exists():
                raise ExistsError('Tenant URL already exists.')
            # time_string = str(int(time.time()))
            # Must be valid postgres schema characters see:
            # https://www.postgresql.org/docs/9.2/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
            # We generate unique schema names each time so we can keep tenants around without
            # taking up url/schema namespace.
            schema_name = '{}'.format(tenant_slug)
            domain = None
            tenant = None
            try:
                subscription = Subscription.objects.create()

                tenant = Tenant.objects.create(name=name,
                                               slug=tenant_slug,
                                               schema_name=schema_name,
                                               subscription=subscription,
                                               owner=user,
                                               is_template=True,
                                               type=type)
                domain = get_tenant_domain_model().objects.create(domain=tenant_domain,
                                                                  tenant=tenant,
                                                                  is_primary=True)
                tenant.add_user(user, is_superuser=True, is_staff=is_staff)
                tenant.auto_create_schema = False
                tenant.save()
                # Create cursor
                sweetify.success(request, "Successfully Created Tenant!", icon='success', timer=5000)
                # messages.success(request, "Successfully Added Tenant!")
                return redirect("template_list")
            except Exception:
                if domain is not None:
                    domain.delete()
                if tenant is not None:
                    # Flag is set to auto-drop the schema for the tenant
                    tenant.delete(True)
                raise
                return tenant_domain
        # return super().post(request, *args, **kwargs)


class UpdateTemplateView(LoginRequiredMixin ,AdminUpdateView):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('template_list', urlconf="multitenancy.urls")
    template_name = 'multitenancy/apps/update_template.html'


class DeleteTemplateView(LoginRequiredMixin ,AdminDeleteView):
    model = Tenant
    template_name = "multitenancy/apps/delete_tenant.html"
    success_url = reverse_lazy("template_list", urlconf="multitenancy.urls")

    def delete(self, request, *args, **kwargs):
        tenant_id = self.kwargs['pk']

        tenant = Tenant.objects.filter(id=tenant_id)
        tenant.delete()
        return HttpResponseRedirect(reverse('tenant_list', urlconf="multitenancy.urls"))



class TenantListView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/apps/tenant_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = TenantFilter(self.request.GET, queryset=Tenant.objects.filter().exclude(is_template=True))
        context['filter'] = f
        return context
    

class CustomerTenantListView(LoginRequiredMixin, CustomerTemplateView):
    template_name = "multitenancy/admin/publicUser/subscriptions.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        subscriptions = TenantFilter(queryset=Tenant.objects.filter(owner=self.request.user))
        context['filter'] = subscriptions
        return context
    

class CreateService(LoginRequiredMixin, CustomerView):
    def get(self,request):
        plans = Plan.objects.all()
        settings.STATICFILES_DIRS = [
            os.path.join(settings.PROJECT_DIR, 'templates/client/static/'),
        ]
        settings.TENANT_CREATION_TEMPLATE ="client/static/publicUser/index.html"
        return render(request,settings.TENANT_CREATION_TEMPLATE, {"plans":plans})

class TenantTemplateViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    model = Tenant
    
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q") 
        queryset = Tenant.objects.filter(is_template=True).search(query=query)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


