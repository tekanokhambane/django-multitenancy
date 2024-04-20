import json
import uuid
from django.views.generic import View
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls.base import reverse, reverse_lazy
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings
from tenant_users.tenants.utils import get_tenant_model, get_tenant_domain_model
from tenant_users.tenants.models import InactiveError, ExistsError
import sweetify
from account.mixins import LoginRequiredMixin
from multitenancy.subscriptions.filters import PlanFilter
from multitenancy.subscriptions.forms import PlanForm, ProductFeatureForm
from multitenancy.subscriptions.models import (
    Plan,
    ProductType,
    Subscription,
    ProductFeature,
)
from multitenancy.apps.models import Tenant
from multitenancy.subscriptions.serializers import (
    PlanSerialiser,
    ProductTypeSerializer,
    SubscriptionSerializer,
)
from multitenancy.admin.views.baseViews import CustomerView
from multitenancy.admin.views.baseViews import (
    AdminListView,
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    AdminView,
    AdminDetailView,
)


class PlanListView(LoginRequiredMixin, AdminTemplateView):

    template_name = "multitenancy/subscriptions/plan_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = PlanFilter(self.request.GET, queryset=Plan.objects.all())
        context["filter"] = f
        return context


class CreatePlanView(LoginRequiredMixin, AdminCreateView):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy("plan_list", urlconf="multitenancy.urls")
    template_name = "multitenancy/subscriptions/create_plan.html"


class PlanDetailView(LoginRequiredMixin, AdminDetailView):
    template_name = "multitenancy/subscriptions/plan_detail.html"
    model = Plan
    # context_object_name = "plan"
    # slug_field = "slug"
    # def get_context_data(self, slug,*args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     plan = Plan.objects.get(slug=slug)
    #     print(plan.features)
    #     context['plan'] = plan
    #     context['form'] =  ProductFeatureForm()
    #     return context


class FeatureCreateView(LoginRequiredMixin, AdminView):

    def post(self, request, *args: str, **kwargs):
        if request.method != "POST":
            return HttpResponseRedirect("Method Not Allowed")
        else:
            form = ProductFeatureForm(request.POST)
            print(request.content_params)
            if form.is_valid():
                name = form.cleaned_data["name"]
                description = form.cleaned_data["description"]

                plan_name = form.cleaned_data["plan_name"]
                plan = form.cleaned_data["plan"]
                feature = None

                try:
                    feature = ProductFeature.objects.create(
                        name=name, description=description
                    )
                    feature.save()
                    print(feature.pk)
                    feature_plan = Plan.objects.get(id=plan)
                    feature_plan.features.add(feature)
                    print(feature_plan.pk)
                    feature_plan.add_feature(feature.pk)

                    sweetify.success(
                        request,
                        "Successfully Added Feature!",
                        icon="success",
                        timer=5000,
                    )
                    return HttpResponseRedirect(f"/admin/settings/plans/{plan_name}/")
                except:
                    sweetify.error(request, "Failed to Add Feature!")
                    return HttpResponseRedirect(f"/admin/settings/plans/{plan_name}/")
            else:
                form = ProductFeatureForm(request.POST)
                return render(
                    request,
                    "multitenancy/subscriptions/plan_detail.html",
                    {"feature_form": form},
                )


class UpdatePlanView(LoginRequiredMixin, AdminUpdateView):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy("plan_list", urlconf="multitenancy.urls")
    template_name = "multitenancy/subscriptions/update_plan.html"


class DeletePlanView(LoginRequiredMixin, AdminDeleteView):
    model = Plan
    template_name = "multitenancy/subscriptions/delete_plan.html"
    success_url = reverse_lazy("plan_list", urlconf="multitenancy.urls")


class SubscriptionsListView(LoginRequiredMixin, AdminListView):
    model = Subscription
    template_name = "multitenancy/subscriptions/subscriptions_list.html"


class PlanViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Plan.objects.all()
    serializer_class = PlanSerialiser
    # permission_classes = [permissions.IsAuthenticated,
    #                       permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductTypeListView(LoginRequiredMixin, AdminListView):
    model = ProductType

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["object_list"] = ProductType.objects.all()
        return context

    template_name = "multitenancy/subscriptions/product_type_list.html"


class SubscriptionsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "plans": reverse("plan-list", request=request, format=format),
            "subscriptions": reverse(
                "subscription-list", request=request, format=format
            ),
        }
    )


class PlanView(CustomerView):

    def post(self, request):
        data = json.loads(request.body)
        duration = data.get("subscription_duration")
        plan = data.get("plan")
        plan_type = Plan.objects.get(id=plan)
        type = plan_type.name
        user = request.user
        randon_id = str(uuid.uuid1())

        tenant_slug = f"{user.username}{randon_id}"
        print(tenant_slug)
        if not user.is_active:
            raise InactiveError("Inactive user passed to provision tenant")
        tenant_domain = "{}.{}".format(tenant_slug, settings.TENANT_USERS_DOMAIN)
        DomainModel = get_tenant_domain_model()
        if DomainModel.objects.filter(domain=tenant_domain).exists():
            raise ExistsError("Tenant URL already exists.")

        schema_name = "{}".format(tenant_slug)
        domain = None
        tenant = None
        try:
            subscription = Subscription.objects.create()
            subscription.start_subscription("monthly")

            tenant = Tenant.objects.create(
                name=tenant_domain,
                slug=tenant_slug,
                schema_name=schema_name,
                subscription=subscription,
                owner=user,
                is_template=True,
                type=type,
            )
            domain = get_tenant_domain_model().objects.create(
                domain=tenant_domain, tenant=tenant, is_primary=True
            )
            tenant.add_user(user, is_superuser=True, is_staff=True)
            tenant.auto_create_schema = False
            tenant.save()
            # Create cursor
            sweetify.success(
                request, "Successfully Created Tenant!", icon="success", timer=5000
            )

            # Do something with the selected plan and duration
            # e.g. create a new subscription in the database
            return JsonResponse({"plan": plan, "subscription_duration": duration})
        except Exception:
            if domain is not None:
                domain.delete()
            if tenant is not None:
                # Flag is set to auto-drop the schema for the tenant
                tenant.delete(True)
            raise
            return tenant_domain
