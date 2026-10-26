from django.contrib import admin
from .models import *
from core.models import CoreUser
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_id",
        "full_name",
        "qualification",
        "specialist",
        "created_at",
    )

    list_filter = (
        "specialist",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "doctor_id",
        "qualification",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    autocomplete_fields = ("user",)

    @admin.display(description="Name", ordering="user__first_name")
    def full_name(self, obj):
        return obj.user.get_full_name() or "-"

    @admin.display(description="Email", ordering="user__email")
    def email(self, obj):
        return obj.user.email