from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('login/', views.sysLogin, name='login'),
    path('signupuser/', views.signupUser, name='signupuser'),
    path('logout/', views.sysLogout, name='logout'),
    path('beds/', views.bedsMmanager, name='beds'),
    path('patients/', views.patientsMmanager, name='patients'),
    path('patients/list/', views.patientsList, name='patients_list'),
]