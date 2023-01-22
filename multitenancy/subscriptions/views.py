import json
from django.views.generic import View
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from multitenancy.subscriptions.models import Plan, ProductType, Subscription
from multitenancy.subscriptions.serializers import PlanSerialiser

@api_view(["GET"])
def get_plans(request):
    qs = Plan.objects.all()
    serializer = PlanSerialiser(qs, many=True)
    return Response(serializer.data)


class PlanView(View):

    def post(self, request):
        data = json.loads(request.body)
        duration = data.get('subscription_duration')
        plan = data.get('plan')
        
        
        # Do something with the selected plan and duration
        # e.g. create a new subscription in the database
        return JsonResponse({"plan": plan, "subscription_duration": duration})
