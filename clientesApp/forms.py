# forms.py
from django import forms
from CarritoApp.models import Clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['iidcliente', 'snombrecliente','sapellidocliente','idni']  # Lista de campos que deseas incluir en el formulario
        widgets = {
            'snombrecliente': forms.TextInput(attrs={'class': 'form-control'}),
            'sapellidocliente': forms.EmailInput(attrs={'class': 'form-control'}),
        }

  