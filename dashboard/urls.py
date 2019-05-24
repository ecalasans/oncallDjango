from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:numero>/', views.details, name='details'),
]