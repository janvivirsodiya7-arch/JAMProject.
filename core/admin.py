from django.contrib import admin
from .models import CoreUser
# Register your models here.


@admin.register(CoreUser)
class CoreUserAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    @admin.display(description="Name", ordering="user__first_name")
    def full_name(self, obj):
        return obj.get_full_name() or "-"

    @admin.display(description="Email", ordering="user__email")
    def email(self, obj):
        return obj.email