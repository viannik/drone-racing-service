from django.urls import path, include

from .views import (
    PilotListView,
    PilotDetailView,
    PilotCreateView,
    PilotUpdateView,
    PilotDeleteView,
)

app_name = "pilots"

urlpatterns = [
    path(
        "pilots/",
        include("django.contrib.auth.urls"),
    ),

    # Pilot URLs
    path(
        "pilots/",
        PilotListView.as_view(),
        name="pilot-list",
    ),
    path(
        "pilots/<int:pk>/",
        PilotDetailView.as_view(),
        name="pilot-detail",
    ),
    path(
        "pilots/create/",
        PilotCreateView.as_view(),
        name="pilot-create",
    ),
    path(
        "pilots/<int:pk>/update/",
        PilotUpdateView.as_view(),
        name="pilot-update",
    ),
    path(
        "pilots/<int:pk>/delete/",
        PilotDeleteView.as_view(),
        name="pilot-delete",
    ),
]