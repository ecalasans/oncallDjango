from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('registration/', views.LoginView.as_view()),
    path('medicos/', views.CreateUser.as_view(), name='criaUsuario'),
]