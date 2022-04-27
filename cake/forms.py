from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class OrderForm(forms.Form):
    count_levels = forms.ChoiceField(
        label="Количество уровней",
        #choices=,
        widget=forms.RadioSelect
    )

