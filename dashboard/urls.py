from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('login/', views.sysLogin, name='login'),
    path('signupuser/', views.signupUser, name='signupuser'),
    path('logout/', views.sysLogout, name='logout'),
    path('beds/', views.beds_manager, name='beds'),
    path('patients/', views.patients_manager, name='patients'),
]