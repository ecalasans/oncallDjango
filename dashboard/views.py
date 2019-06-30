from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    template_name = 'registration/login.html'
    extra_context = {
        'next': '/dashboard',
    }

class MainView(TemplateView):
    template_name = 'dashboard/index.html'
