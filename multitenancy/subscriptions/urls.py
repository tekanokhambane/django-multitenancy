from django.urls import path
from . import views

urlpatterns = [
    path('multitenancy/plans', views.get_plans)
]