from django.urls import path
from . import views

urlpatterns = [
    path("settings/plans/", views.PlanListView.as_view(), name="plan_list"),
    path("settings/plans/<str:slug>/", views.PlanDetailView.as_view(), name="plan_detail"),
    path("settings/plans/feature/create/", views.FeatureCreateView.as_view(), name="create_feature"),
    path("settings/plans/<int:pk>/update/", views.UpdatePlanView.as_view(), name="update_plan"),
    path("settings/plan/create/", views.CreatePlanView.as_view(), name="create_plan"),
    path("settings/plans/<int:pk>/delete/", views.DeletePlanView.as_view(), name="delete_plan"),
    path("settings/usersubscriptions/", views.UserSubscriptionsListView.as_view(), name="usersubscription_list"),
    path("settings/producttypes/", views.ProductTypeListView.as_view(), name="producttype_list"),

]