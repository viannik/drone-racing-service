from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Pilot
from racing.models import Drone, RaceTrack, Manufacturer

from .forms import (
    DroneForm,
    DroneModelSearchForm,
    ManufacturerNameSearchForm,
    RaceTrackNameSearchForm,
)


@login_required
def index(request):
    num_pilots = Pilot.objects.count()
    num_drones = Drone.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_race_tracks = RaceTrack.objects.count()
    top_pilots = Pilot.objects.order_by('-skill_rating')[:5]

    from django.db.models import Count
    popular_drones = Drone.objects.annotate(
        pilot_count=Count('pilots')
    ).order_by('-pilot_count')[:5]

    context = {
        "num_pilots": num_pilots,
        "num_drones": num_drones,
        "num_manufacturers": num_manufacturers,
        "num_race_tracks": num_race_tracks,
        "top_pilots": top_pilots,
        "popular_drones": popular_drones,
    }

    return render(request, "racing/index.html", context=context)


# Manufacturer Views
class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "racing/manufacturer_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        from django.db.models import Count
        form = ManufacturerNameSearchForm(self.request.GET)
        queryset = Manufacturer.objects.all().annotate(drone_count=Count('drones'))
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer
    context_object_name = "manufacturer"
    template_name = "racing/manufacturer_detail.html"
    queryset = Manufacturer.objects.prefetch_related("drones__pilots")


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("racing:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("racing:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("racing:manufacturer-list")


# RaceTrack Views
class RaceTrackListView(LoginRequiredMixin, generic.ListView):
    model = RaceTrack
    context_object_name = "racetrack_list"
    template_name = "racing/racetrack_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = RaceTrackNameSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = RaceTrackNameSearchForm(self.request.GET)
        queryset = RaceTrack.objects.all()
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class RaceTrackDetailView(LoginRequiredMixin, generic.DetailView):
    model = RaceTrack
    context_object_name = "racetrack"
    template_name = "racing/racetrack_detail.html"


class RaceTrackCreateView(LoginRequiredMixin, generic.CreateView):
    model = RaceTrack
    fields = "__all__"
    success_url = reverse_lazy("racing:racetrack-list")


class RaceTrackUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = RaceTrack
    fields = "__all__"
    success_url = reverse_lazy("racing:racetrack-list")


class RaceTrackDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = RaceTrack
    success_url = reverse_lazy("racing:racetrack-list")


# Drone Views
class DroneListView(LoginRequiredMixin, generic.ListView):
    model = Drone
    paginate_by = 5
    queryset = (Drone.objects
                .select_related("manufacturer")
                .prefetch_related("pilots"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.request.GET.get("model_name", "")
        context["search_form"] = DroneModelSearchForm(
            initial={"model_name": model_name}
        )
        if self.request.user.is_authenticated:
            context["user_drone_ids"] = set(
                self.request.user.drones.values_list('id', flat=True)
            )
        else:
            context["user_drone_ids"] = set()
        return context

    def get_queryset(self):
        form = DroneModelSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                model_name__icontains=form.cleaned_data["model_name"]
            )
        return self.queryset


class DroneDetailView(LoginRequiredMixin, generic.DetailView):
    model = Drone
    queryset = (Drone.objects
                .select_related("manufacturer")
                .prefetch_related("pilots"))


class DroneCreateView(LoginRequiredMixin, generic.CreateView):
    model = Drone
    form_class = DroneForm
    success_url = reverse_lazy("racing:drone-list")


class DroneUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Drone
    form_class = DroneForm
    success_url = reverse_lazy("racing:drone-list")


class DroneDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Drone
    success_url = reverse_lazy("racing:drone-list")


@login_required
def toggle_assign_to_drone(request, pk):
    pilot = (Pilot.objects
             .prefetch_related("drones")
             .get(id=request.user.id))
    drone = (Drone.objects
             .prefetch_related("pilots")
             .get(id=pk))

    if drone in pilot.drones.all():
        pilot.drones.remove(pk)
    else:
        pilot.drones.add(pk)

    return redirect(request.META.get('HTTP_REFERER',
                                     reverse_lazy("racing:drone-list")))