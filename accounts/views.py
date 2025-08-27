from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Pilot

from .forms import PilotCreationForm, PilotUpdateForm, PilotUsernameSearchForm

# Pilot Views
class PilotListView(LoginRequiredMixin, generic.ListView):
    model = Pilot
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = PilotUsernameSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        form = PilotUsernameSearchForm(self.request.GET)
        queryset = Pilot.objects.all().prefetch_related("drones")
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class PilotDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pilot
    queryset = Pilot.objects.prefetch_related("drones__manufacturer")


class PilotCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pilot
    form_class = PilotCreationForm
    success_url = reverse_lazy("pilots:pilot-list")


class PilotUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pilot
    form_class = PilotUpdateForm
    success_url = reverse_lazy("pilots:pilot-list")


class PilotDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Pilot
    success_url = reverse_lazy("pilots:pilot-list")
