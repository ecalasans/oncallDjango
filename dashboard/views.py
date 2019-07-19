from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView, RedirectView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from dashboard.models import Leito, Hospital, Paciente_Leito, Setor
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import MedicoForm, PacienteForm
from bootstrap_modal_forms.generic import BSModalCreateView

class LoginView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    template_name = 'registration/login.html'

    hospitais = Hospital.objects.all().order_by('nome')

    extra_context = {
        'next': '/dashboard',
        'hospitais': hospitais,
    }

#Classe de logout
class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class MainView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)

        hosp = Hospital.objects.get(sigla='HJPB')

        setores = Setor.objects.filter(hospital_id=hosp)

        leitos = {}

        for setor in setores:
            leitos[setor] = Leito.objects.filter(hospital_id=hosp, setor_id=setor.id).values('status')\
                .annotate(Count('setor'))

        context = {
            'setores': setores,
            'leitos': leitos,
        }

        return context

#Pacientes
#Criação
class CreatePaciente(CreateView):
    template_name = 'dashboard/pacientes/create.html'
    form_class = PacienteForm

    def get_context_data(self, **kwargs):
        context = super(CreatePaciente).get_context_data(**kwargs)

        return context



#Médicos
#Criação
# class CreateUser(CreateView):
#     template_name = 'dashboard/medicos/medicos.html'
#     form_class = MedicoForm
#     success_url = 'success/'
#
#     def get_context_data(self, **kwargs):
#         context = super(CreateUser, self).get_context_data(**kwargs)
#
#         hospitais = Hospital.objects.all().order_by('id')
#
#         form = MedicoForm()
#
#         context['form'] = form
#         context['hospitais'] = hospitais
#
#         return context

class CreateUser(BSModalCreateView):
    template_name = 'dashboard/medicos/modal.html'
    form_class = MedicoForm
    success_message = "Você foi cadastrado com sucesso!!"
    success_url = '/'

