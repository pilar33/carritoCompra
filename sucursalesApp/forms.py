from django import forms
from django.utils import timezone
from CarritoApp.models import Sucursales

class SucursalForm(forms.ModelForm):
    created_at = forms.DateTimeField(initial=timezone.now, label='Fecha y Hora creación', required=True)

    class Meta:
        model = Sucursales
        fields = ['iidsucursal', 'snombre', 'iidestado', 'created_at']
        exclude = ['updated_at']

    def save(self, commit=True):
        return super().save(commit=commit)
