import django_filters
from django import forms
from .models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(
        field_name="patient__email",
        lookup_expr="iexact",
        label="Email",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )

    appointment_id = django_filters.CharFilter(
        field_name="appointment_id",
        lookup_expr="iexact",
        label="Appointment ID",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "ID",
            }
        ),
    )

    date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="exact",
        label="Date",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
        }),
    )

    class Meta:
        model = Appointment
        fields = ["email", "appointment_id", "date"]


