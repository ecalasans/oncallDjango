from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView, RedirectView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from dashboard.models import Leito, Hospital


class LoginView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    template_name = 'registration/login.html'
    extra_context = {
        'next': '/dashboard',
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

        leitos = Leito.objects.filter(hospital_id=hosp)

        context = {
            'utin1_ocup' : leitos.filter(setor_id=1, status='O').count(),
            'utin1_vago': leitos.filter(setor_id=1, status='L').count(),
            'utin1_bloq': leitos.filter(setor_id=1, status='B').count(),
            'utin2_ocup': leitos.filter(setor_id=2, status='O').count(),
            'utin2_vago': leitos.filter(setor_id=2, status='L').count(),
            'utin2_bloq': leitos.filter(setor_id=2, status='B').count(),
            'mr_ocup': leitos.filter(setor_id=3, status='O').count(),
            'mr_vago': leitos.filter(setor_id=3, status='L').count(),
            'mr_bloq': leitos.filter(setor_id=3, status='B').count(),
        }

        return context