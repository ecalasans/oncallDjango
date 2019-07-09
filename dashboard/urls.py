from django.urls import path
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('registration/', views.LoginView.as_view()),
    path('medicos/', views.CreateUser.as_view(), name='criaUsuario')
    #path('<int:numero>/', views.details, name='details'),
]