from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class PilotCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "drone_license",
            "skill_rating",
            "certification_date",
        )


class PilotUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "drone_license",
            "skill_rating",
            "certification_date",
        )


class PilotUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=127, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by username...'
        })
    )