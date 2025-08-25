from django.contrib import admin

from racing.models import Manufacturer, Drone, RaceTrack


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "max_speed",
        "weight",
        "manufacturer",
    )
    search_fields = (
        "model_name",
        "manufacturer__name",
    )
    list_filter = ("manufacturer",)


@admin.register(RaceTrack)
class RaceTrackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "difficulty_level",
        "length_meters",
        "location",
    )
    search_fields = ("name", "location")
    list_filter = ("difficulty_level",)