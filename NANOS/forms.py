from django import forms
from API.models import NanoIoT


class AddNewNanoForm(forms.ModelForm):
    class Meta:
        model = NanoIoT
        fields = ['hostname', 'where']
        widgets = {
            'hostname': forms.TextInput(attrs={'class': 'ml-3 mr-5 center col-3'}),
            'where': forms.Select(attrs={'class': 'ml-3 mr-5 col-3'})
        }
