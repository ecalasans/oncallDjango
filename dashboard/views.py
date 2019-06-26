from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView

def index(request):
    context = {}

    return render(request, 'dashboard/index.html', context)

def details(request, numero):
    return HttpResponse("ID do leito: %s" % numero)
