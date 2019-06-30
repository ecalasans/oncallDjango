from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


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
