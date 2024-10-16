from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from CarritoApp.models import Clientes,TipoCliente

class CustomLoginForm(AuthenticationForm):
    # Puedes personalizar el formulario aquí si es necesario

    # Agregar campos adicionales o personalizar los campos existentes
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario:'}),
		error_messages={'required': 'El nombre de usuario es obligatorio.'}
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña:'}),
    )

class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)
    # Agrega el campo de selección desde el modelo TipoCliente
	iidtipocliente = forms.ModelChoiceField(queryset=TipoCliente.objects.all(), required=False)
    # Agrega el campo de entrada para el idni
	idni = forms.IntegerField(required=False)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email
	
	def save(self, commit=True):
		user = super().save(commit=False)
		user.save()        
        # Guarda el campo de selección en el modelo Clientes
		iidtipocliente = self.cleaned_data.get('iidtipocliente')
		idni = self.cleaned_data.get('idni')
		if iidtipocliente:
			cliente = Clientes.objects.create(
                user=user,
                iidtipocliente=iidtipocliente,
				# Agrega otros campos según sea necesario
				snombrecliente=user.first_name,
                sapellidocliente=user.last_name,
				iidestado = 1,#POR DEFECTO ACTIVO
				idni=idni,
                user_id = user.id,
            )
		
		

        # Una vez que el usuario se ha guardado en la base de datos, agrégalo al grupo "Usuario" por defecto
		grupo_usuario, created = Group.objects.get_or_create(name='Usuario')
		user.groups.add(grupo_usuario)
		return user
       
