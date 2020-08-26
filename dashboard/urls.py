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
    path('patients/record/', views.patientsRecord, name="patients_record"),
    path('patients/occurrence/', views.patientsOpenOccurrence, name='patients_open_occurrence'),
]