from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('login/', views.sysLogin, name='login'),
    path('signupuser/', views.signupUser, name='signupuser'),
    path('logout/', views.sysLogout, name='logout'),
    path('beds/', views.bedsMmanager, name='beds'),
    path('patients/', views.patientsManager, name='patients'),
    path('patients/get_paciente/', views.getPaciente, name='get_paciente'),
    path('patients/list/', views.patientsList, name='patients_list'),
    path('patiens/discharge/', views.patientsDischarge, name='patients_discharge'),
    path('patients/update/', views.patientUpdate, name='patients_update'),
    path('patients/record/', views.patientsRecord, name="patients_record"),
    path('patients/occurrence/', views.patientsOpenOccurrence, name='patients_open_occurrence'),
    path('history/', views.history, name='history'),
    path('history/get_ocurrencies', views.getOccurencies, name='history_get_ocurrencies'),
    path('history/occurrency', views.Ocurrency, name='history_ocurrency'),
    path('echoserver/', views.echoServer, name='eco_servidor'),
]