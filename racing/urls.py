from django.urls import path

from .views import (
    index,
    DroneListView,
    DroneDetailView,
    DroneCreateView,
    DroneUpdateView,
    DroneDeleteView,
    ManufacturerListView,
    ManufacturerDetailView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    RaceTrackListView,
    RaceTrackDetailView,
    RaceTrackCreateView,
    RaceTrackUpdateView,
    RaceTrackDeleteView,
    toggle_assign_to_drone,
)

app_name = "racing"

urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    # Manufacturer URLs
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "manufacturers/<int:pk>/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "manufacturers/<int:pk>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
    # RaceTrack URLs
    path(
        "racetracks/",
        RaceTrackListView.as_view(),
        name="racetrack-list",
    ),
    path(
        "racetracks/<int:pk>/",
        RaceTrackDetailView.as_view(),
        name="racetrack-detail",
    ),
    path(
        "racetracks/create/",
        RaceTrackCreateView.as_view(),
        name="racetrack-create",
    ),
    path(
        "racetracks/<int:pk>/update/",
        RaceTrackUpdateView.as_view(),
        name="racetrack-update",
    ),
    path(
        "racetracks/<int:pk>/delete/",
        RaceTrackDeleteView.as_view(),
        name="racetrack-delete",
    ),
    # Drone URLs
    path(
        "drones/",
        DroneListView.as_view(),
        name="drone-list",
    ),
    path(
        "drones/<int:pk>/",
        DroneDetailView.as_view(),
        name="drone-detail",
    ),
    path(
        "drones/create/",
        DroneCreateView.as_view(),
        name="drone-create",
    ),
    path(
        "drones/<int:pk>/update/",
        DroneUpdateView.as_view(),
        name="drone-update",
    ),
    path(
        "drones/<int:pk>/delete/",
        DroneDeleteView.as_view(),
        name="drone-delete",
    ),

    # Toggle assignment of a pilot to a drone
    path(
        "drones/<int:pk>/toggle-assign/",
        toggle_assign_to_drone,
        name="toggle-drone-assign",
    ),
]
