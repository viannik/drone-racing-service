from django.contrib import admin

from accounts.models import Pilot


@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "drone_license",
        "skill_rating",
        "certification_date",
    )
    search_fields = (
        "username",
        "drone_license",
    )
    list_filter = ("skill_rating",)