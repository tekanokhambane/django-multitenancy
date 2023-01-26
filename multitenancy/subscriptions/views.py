import json
from django.views.generic import View
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from multitenancy.subscriptions.models import Plan, ProductType, Subscription
from multitenancy.apps.models import Tenant
from multitenancy.subscriptions.serializers import PlanSerialiser
from multitenancy.admin.views.customerViews import CustomerView

@api_view(["GET"])
def get_plans(request):
    qs = Plan.objects.all()
    serializer = PlanSerialiser(qs, many=True)
    return Response(serializer.data)


class PlanView(CustomerView):

    def post(self, request):
        data = json.loads(request.body)
        duration = data.get('subscription_duration')
        plan = data.get('plan')
        
        subscription = Subscription.objects.create()
        subscription.save()
        service = Tenant.objects.create()
        # Do something with the selected plan and duration
        # e.g. create a new subscription in the database
        return JsonResponse({"plan": plan, "subscription_duration": duration})
