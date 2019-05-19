from django.db import models
from django.utils import timezone


class Setor(models.Model):
    setor = models.CharField(default="", max_length=10)

    def __str__(self):
        return self.setor

class Leito(models.Model):
    situacao = models.CharField(default="A", max_length=2) #A - ativo, D = desativado
    status = models.CharField(default="L", max_length=2) #L - livre, O = ocupado, B = bloqueado

    def __str__(self):
        return "Leito " + str(self.id) + "(" + self.situacao + " - " + self.status + ")"

class Medico(models.Model):
    crm = models.CharField(default="", max_length=6)
    email = models.EmailField(default="", max_length=100)

class Paciente(models.Model):
    nome = models.CharField(max_length=250, default="")
    ig = models.CharField(max_length=10, default="")
    idade = models.CharField(default="", max_length=10)
    peso_nasc = models.IntegerField(default=0)
    peso_atual = models.IntegerField(default=0)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING)

class Paciente_Leito(models.Model):
    pac = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING)
    leito = models.ForeignKey(Leito, on_delete=models.DO_NOTHING)

class Ocorrencia(models.Model):
    pac = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING)
    med = models.ForeignKey(Medico, on_delete=models.DO_NOTHING)
    diagnostico = models.TextField(default="", max_length=300)
    dieta = models.CharField(default="", max_length=100)
    acesso_venoso = models.CharField(default="Não", max_length=5)
    antibiotico = models.CharField(default="Não", max_length=5)
    medicamentos = models.TextField(default="", max_length=400)
    ventilacao = models.CharField(default="Ar ambiente", max_length=100)
    fototerapia = models.CharField(default="Não", max_length=5)
    exames = models.TextField(default="", max_length=500)
    conduta = models.TextField(default="", max_length=500)
    data_add = models.DateTimeField(editable=False, default=timezone.now())
    data_modif = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            self.data_add = timezone.now()
        self.data_modif = timezone.now()

        return super(Ocorrencia, self).save(*args, **kwargs)

