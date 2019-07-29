from django import forms
from .models import Paciente_Leito, Medico, Hospital
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django_select2.forms import Select2MultipleWidget

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente_Leito
        fields =['nome', 'ig', 'peso_nasc', 'peso_atual', 'idade', 'leito',]

class UsuarioForm(forms.ModelForm):
    hospitais = forms.ModelMultipleChoiceField(queryset=Hospital.objects.all(), widget=Select2MultipleWidget)

    class Meta:
        model = Medico
        fields = ['crm', 'username', 'first_name', 'last_name', 'email', 'password',
                  'is_active', 'hospitais',]


    def save(self, commit=True):
        medico = super(UsuarioForm, self).save(commit=False)

        pass_raw = self.cleaned_data['password']

        medico.set_password(pass_raw)

        medico.is_active = False

        if commit:
            medico.save()

        return medico

