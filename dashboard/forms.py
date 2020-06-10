from django.forms import ModelForm, ValidationError, Select, IntegerField
from .models import Medico, Hospital, Leito, Paciente, Setor
import re

class MedicoForm(ModelForm):
    class Meta:
        model = Medico
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'crm', 'hospital']
        widgets ={
            'hospital': Select()
        }

    def clean_username(self):
        if len(self.cleaned_data['username']) == 0:
            raise ValidationError('Este campo é requerido!')
        else:
            return self.cleaned_data['username']

    def clean_first_name(self):
        if len(self.cleaned_data['first_name']) == 0:
            raise ValidationError('Este campo é requerido!')
        else:
            return self.cleaned_data['first_name']

    def clean_last_name(self):
        if len(self.cleaned_data['last_name']) == 0:
            raise ValidationError('Este campo é requerido!')
        else:
            return self.cleaned_data['last_name']

    def clean_email(self):
        if len(self.cleaned_data['username']) == 0:
            raise ValidationError('Este campo é requerido!')
        else:
            return self.cleaned_data['email']

    def clean_crm(self):
        if len(self.cleaned_data['crm']) == 0:
            raise ValidationError('Este campo é requerido!')
        else:
            regex_crm = re.compile('[0-9]+')
            if (regex_crm.match(self.cleaned_data['crm'])) is not None:
                return self.cleaned_data['crm']
            else:
                raise ValidationError('Só pode conter números!!')

    def clean_password(self):
        regex_pass = re.compile('[a-zA-Z0-9!@#$%*_]+')

        if len(self.cleaned_data['password']) >= 8:
            #Verifica o padrão da senha
            if regex_pass.match(self.cleaned_data['password']) is not None:
                return self.cleaned_data['password']
            else:
                raise ValidationError('Senha deve conter apenas alfanuméricos ou \n !@#$%*_')
        else:
           raise ValidationError('Senha deve ter pelo menos 8 caracteres!')

class LeitoForm(ModelForm):
    class Meta:
        model = Leito
        fields = ['situacao', 'status']
        widgets = {
            'situacao': Select(choices=[('A', 'Ativo'), ('D', 'Desativado')]),
            'status': Select(choices=[('L', 'Livre'), ('O', 'Ocupado'), ('B', 'Bloqueado')])
        }

class PacienteForm(ModelForm):
    setor = IntegerField()
    leito = IntegerField()
    class Meta:
        model = Paciente
        fields = ['nome', 'ig', 'idade', 'peso_nasc', 'peso_atual', 'tcle']

    # def clean_nome(self):
    #     if len(self.cleaned_data['nome']) == 0:
    #         raise ValidationError('Esse campo é requerido')
    #     else:
    #         return self.cleaned_data['nome']

    # def clean_ig(self):
    #     regex_ig = re.compile('([2-4][0-9])sem|([0-6]d)')
    #
    #     if regex_ig.match(self.cleaned_data['ig']) is not None:
    #         return self.cleaned_data['ig']
    #     else:
    #         raise ValidationError('Dado fora do padrão:  observe o exemplo!')
    #
    # def clean_idade(self):
    #     regex_idade = re.compile('([0-1][aA]{1})?([0-1]?[0-9][mM])?([0-2]?[0-9][dD])?')
    #
    #     if regex_idade.match(self.cleaned_data['idade']) is not None:
    #         return self.cleaned_data['idade']
    #     else:
    #         raise ValidationError('Dado fora do padrão:  observe o exemplo!')