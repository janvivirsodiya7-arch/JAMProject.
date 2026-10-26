
from django.urls import path

from . import views

app_name = "appointment"

urlpatterns = [
    path(
        "list/",
        views.appointment_list,
        name="appointment_list"
    ),

    path(
        "create/",
        views.appointment_create,
        name="appointment_create"
    ),

    path(
        'detail/<int:pk>/',
        views.appointment_detail,
        name='appointment_detail'
),

    path(
        "update/<int:pk>/",
        views.appointment_update,
        name="appointment_update"
    ),

    path(
        "delete/<int:pk>/",
        views.appointment_delete,
        name="appointment_delete"
    ),

    path("treatment/", 
         views.treatment_list, 
         name="treatment_list"
    )
]



