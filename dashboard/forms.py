from django import forms
from .models import Paciente, Medico
from django.contrib.auth.models import User

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'ig', 'idade', 'peso_nasc', 'peso_atual', 'setor',]

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['crm',]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password',]