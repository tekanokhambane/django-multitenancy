from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Client, Domain
from .serializers import ClientSerializer, DomainSerializer
from django.views.decorators.csrf import csrf_exempt
from django_tenants.utils import schema_context
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST', 'PUT'])
def client_list(request):

    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
def domain_list(request):

    if request.method == 'GET':
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DomainSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@api_view(['GET', 'POST', 'PUT'])
#def customer_list(request):

#    if request.method == 'GET':
#        customers = Customer.objects.all()
#        serializer = CustomerSerializer(customers, many=True)
#        return Response(serializer.data)

#    elif request.method == 'POST':
#        serializer = CustomerSerializer(data=request.data)

#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'PUT':
#        serializer = CustomerSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def client_detail(request, client):
    try:
        client = get_object_or_404(Client, client=client)
       # client = Client.object.get(Client=Client)

    except Client.DoesNotExit:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(client, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)
