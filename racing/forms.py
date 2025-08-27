from django import forms
from django.contrib.auth import get_user_model

from racing.models import Drone

class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ["model_name",
                  "max_speed",
                  "weight",
                  "manufacturer",
                  "pilots",]

    pilots = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class ManufacturerNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )


class DroneModelSearchForm(forms.Form):
    model_name = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by model...'
        })
    )


class RaceTrackNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )