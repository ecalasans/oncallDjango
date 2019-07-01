from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'ig', 'idade', 'peso_nasc', 'peso_atual', 'setor']