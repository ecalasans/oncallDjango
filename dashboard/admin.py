from django.contrib import admin

from .models import Leito, Setor, Hospital, Medico


admin.site.register(Leito)
admin.site.register(Setor)
admin.site.register(Hospital)
admin.site.register(Medico)
# Register your models here.
