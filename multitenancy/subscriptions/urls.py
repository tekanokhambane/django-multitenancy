from django.urls import path
from . import views

urlpatterns = [
    path('multitenancy/plans', views.get_plans),
    path('multitenancy/plans/create', views.PlanView.as_view()),
]