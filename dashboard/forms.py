from django.forms import ModelForm
from .models import Medico

class MedicoForm(ModelForm):
    class Meta:
        model = Medico
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'hospital', 'crm']
