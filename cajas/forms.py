from django import forms
from django.forms import ModelForm
from CarritoApp.models import Cajas, Empleados
from django.utils import timezone


class CajasForm(ModelForm):
    #empleado = forms.ModelChoiceField(queryset=Empleados.objects.all(), to_field_name='snombre', label='Nombre y Apellido')
    fechaapertura = forms.DateTimeField(initial=timezone.now, label='Fecha y Hora de Apertura',required=True)  # Asegura que el campo sea requerido)
   
    class Meta:
        model = Cajas
        fields = ['iidsucursal','inrocaja', 'iidtipomovimiento','fechaapertura','fmontoapertura', 'sobservaciones']
        exclude = ['dfechacierre', 'fmontocierre']  # Lista de campos del modelo a excluir del formulario

    def __init__(self, user, *args, **kwargs):
        super(CajasForm, self).__init__(*args, **kwargs)
        self.user = user  # Almacena el usuario en el formulario

    def save(self, commit=True):
        # Obtén el empleado correspondiente al usuario
        empleado = Empleados.objects.get(user=self.user)
        
        # Crea una nueva instancia de Cajas y establece el empleado
        instance = super(CajasForm, self).save(commit=False)
        instance.iidempleado = empleado

        if commit:
            instance.save()

        return instance