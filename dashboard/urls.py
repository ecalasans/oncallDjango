from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('login/', views.sysLogin, name='login'),
    path('signupuser/', views.signupUser, name='signupuser'),
]