from django.contrib import admin

from .models import Leito, Setor, Hospital, Medico, Paciente, Ocorrencia

admin.site.register(Leito)
admin.site.register(Setor)
admin.site.register(Hospital)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Ocorrencia)
# Register your models here.
