import django_filters
from django.db.models import Q

from .models import Doctor


class DoctorFilter(django_filters.FilterSet):

    # ---------------------------------------------------------
    # GENERAL SEARCH
    # ---------------------------------------------------------

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search patient...",
            }
        ),
    )

    # ---------------------------------------------------------
    # DOCTOR FIELDS
    # ---------------------------------------------------------

    doctor_id = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Doctor ID",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Doctor ID",
            }
        ),
    )

    # ---------------------------------------------------------
    # CORE USER FIELDS
    # ---------------------------------------------------------

    email = django_filters.CharFilter(
        field_name="user__email",
        lookup_expr="icontains",
        label="Email",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
    )

    first_name = django_filters.CharFilter(
        field_name="user__first_name",
        lookup_expr="icontains",
        label="First Name",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
            }
        ),
    )

    last_name = django_filters.CharFilter(
        field_name="user__last_name",
        lookup_expr="icontains",
        label="Last Name",
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }
        ),
    )

    # ---------------------------------------------------------
    # CUSTOM SEARCH
    # ---------------------------------------------------------

    def filter_search(self, queryset, name, value):
        """
        Search across multiple Patient + CoreUser fields.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(doctor_id__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(user__email__icontains=value)
        )

    class Meta:
        model = Doctor

        fields = [
            "search",
            "doctor_id",
            "email",
            "first_name",
            "last_name",
        ]




