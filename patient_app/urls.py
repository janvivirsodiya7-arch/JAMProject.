
from django.urls import path

from . import views

app_name = "patient"

urlpatterns = [
    path("list/", views.patient_list, name="patient_list"),
    path("create/", views.patient_create, name="patient_create"),
    path("detail/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("update/<int:pk>/", views.patient_update, name="patient_update"),
    path("delete/<int:pk>/", views.patient_delete, name="patient_delete"),
]
