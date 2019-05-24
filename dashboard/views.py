from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World")

def details(request, numero):
    return HttpResponse("ID do leito: %s" % numero)
