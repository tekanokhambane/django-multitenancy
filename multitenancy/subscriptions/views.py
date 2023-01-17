from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Plan
from .serializers import PlanSerialiser

@api_view(["GET"])
def get_plans(request):
    qs = Plan.objects.all()
    serializer = PlanSerialiser(qs, many=True)
    return Response(serializer.data)
