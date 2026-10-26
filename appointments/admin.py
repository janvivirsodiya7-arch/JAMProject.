from django.contrib import admin
from .models import *
from core.models import CoreUser

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_id",
        "patient_name",
        "doctor_name",
        "status",
        "date",
        "time",
    )

    list_filter = (
        "status",
        "date",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "appointment_id",
        "patient__patient_id",
        "patient__user__first_name",
        "patient__user__last_name",
        "patient__user__email",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "doctor__user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "date"

    ordering = (
        "-date",
        "-time",
    )

    autocomplete_fields = (
        "patient",
        "doctor",
    )

    list_per_page = 25

    @admin.display(description="Patient", ordering="patient__user__first_name")
    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.email

    @admin.display(description="Doctor", ordering="doctor__user__first_name")
    def doctor_name(self, obj):
        return obj.doctor.user.get_full_name() or obj.doctor.user.email
