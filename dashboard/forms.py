from django import forms
from .models import Paciente, Medico
from django.contrib.auth.models import User

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'ig', 'idade', 'peso_nasc', 'peso_atual', 'setor', ]

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['crm', 'username', 'first_name', 'last_name', 'email', 'password', 'hospital', ]

    def save(self, commit=True):
        medico = super(MedicoForm, self).save(commit=False)

        pass_raw = self.cleaned_data['password']

        medico.set_password(pass_raw)

        if commit:
            medico.save()

        return medico