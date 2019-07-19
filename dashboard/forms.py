from django import forms
from .models import Paciente_Leito, Medico
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalForm

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente_Leito
        fields =['nome', 'ig', 'peso_nasc', 'peso_atual', 'idade', 'leito',]

class MedicoForm(BSModalForm):
    class Meta:
        model = Medico
        fields = ['crm', 'username', 'first_name', 'last_name', 'email', 'password', 'hospital',
                  'is_active',]

    def save(self, commit=True):
        medico = super(MedicoForm, self).save(commit=False)

        pass_raw = self.cleaned_data['password']

        medico.set_password(pass_raw)

        medico.is_active = False

        if commit:
            medico.save()

        return medico

