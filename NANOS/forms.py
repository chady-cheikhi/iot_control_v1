from django import forms
from API.models import NanoIoT


class AddNewNanoForm(forms.ModelForm):
    class Meta:
        model = NanoIoT
        fields = ['hostname', 'where']
        attrs = {'class': 'some_class'}
