from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Hospital(models.Model):
    nome = models.CharField(max_length=250, default="")
    sigla = models.CharField(max_length=50, default="")

    def __str__(self):
        return  self.nome

class Setor(models.Model):
    setor = models.CharField(default="", max_length=10)
    hospital = models.ForeignKey(Hospital, on_delete=models.DO_NOTHING, default="")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.setor + ' - ' + str(self.hospital)

class Leito(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.DO_NOTHING, default="")
    numero = models.IntegerField(default=0)
    label = models.CharField(default="", max_length=20, null=True)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING, default="")
    situacao = models.CharField(default="A", max_length=2) #A - ativo, D = desativado
    status = models.CharField(default="L", max_length=2) #L - livre, O = ocupado, B = bloqueado

    def __str__(self):
        if self.label != None:
            return "Leito " + str(self.label) + "(" + self.situacao + " - " + self.status + ") - " \
                   + self.setor.setor + " " + str(self.hospital.sigla)
        else:
            return "Leito " + str(self.numero) + "(" + self.situacao + " - " + self.status + ") - " \
               + self.setor.setor + " " + str(self.hospital.sigla)

class Medico(User):
    crm = models.CharField(null=False, max_length=6)
    hospital = models.ForeignKey(Hospital, on_delete=models.DO_NOTHING, default='')

    def __str__(self):
        return self.first_name + ' '+ self.last_name

class Paciente(models.Model):
    nome = models.CharField(max_length=250, default="")
    ig = models.CharField(max_length=10, default="")
    idade = models.CharField(default="", max_length=10)
    peso_nasc = models.IntegerField(default=0)
    peso_atual = models.IntegerField(default=0)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING, default=None)
    leito = models.ForeignKey(Leito, on_delete=models.DO_NOTHING, default=None)
    tcle = models.BooleanField(default=False)
    status = models.CharField(max_length=1, default="")# I - internado, A - Alta, T - Transferido, O - óbito
    data_add = models.DateTimeField(editable=False, default=timezone.now())
    data_modif = models.DateTimeField(default=timezone.now())
    log_med = models.ForeignKey(Medico, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return self.nome + ' - Leito ' + str(self.leito.numero) + ' - ' \
               + self.leito.setor.setor


class Ocorrencia(models.Model):
    pac = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING)
    med = models.ForeignKey(Medico, on_delete=models.DO_NOTHING)
    diagnostico = models.TextField(default="", max_length=300)
    idade = models.TextField(default="", max_length=20)
    igc = models.TextField(default="", max_length=20)
    peso_nasc = models.IntegerField(default=0)
    peso_atual = models.IntegerField(default=0)
    dieta = models.CharField(default="", max_length=100)
    acesso_venoso = models.CharField(default="Não", max_length=40)
    antibiotico = models.CharField(default="Não", max_length=100)
    medicamentos = models.TextField(default="", max_length=400)
    ventilacao = models.CharField(default="Ar ambiente", max_length=100)
    fototerapia = models.CharField(default="Não", max_length=5)
    vacina = models.CharField(default="N", max_length=2)
    fono = models.CharField(default="N", max_length=2)
    exames = models.TextField(default="", max_length=500)
    conduta = models.TextField(default="", max_length=500)
    recomendacoes = models.TextField(default="", max_length=500)
    data_add = models.DateTimeField(editable=False, default=timezone.now())
    data_modif = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            self.data_add = timezone.now()
        self.data_modif = timezone.now()

        return super(Ocorrencia, self).save(*args, **kwargs)

