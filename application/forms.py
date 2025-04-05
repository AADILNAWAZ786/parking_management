from django import forms
from .models import CategoryEntry

class CategoryEntryForm(forms.ModelForm):
    class Meta:
        model = CategoryEntry
        fields = ['parking_area_no', 'vehicle_type', 'vehicle_limit', 'parking_charge']

class loginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)