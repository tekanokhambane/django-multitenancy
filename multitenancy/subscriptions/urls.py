from django.urls import path
from . import views

urlpatterns = [
    path("billing/plans/", views.PlanListView.as_view(), name="plan_list"),
    path("billing/plans/<str:slug>/", views.PlanDetailView.as_view(), name="plan_detail"),
    path("billing/plans/feature/create/", views.FeatureCreateView.as_view(), name="create_feature"),
    path("billing/plans/<int:pk>/update/", views.UpdatePlanView.as_view(), name="update_plan"),
    path("billing/plan/create/", views.CreatePlanView.as_view(), name="create_plan"),
    path("billing/plans/<int:pk>/delete/", views.DeletePlanView.as_view(), name="delete_plan"),
    path("billing/subscriptions/", views.SubscriptionsListView.as_view(), name="usersubscription_list"),
    path("settings/producttypes/", views.ProductTypeListView.as_view(), name="producttype_list"),

]