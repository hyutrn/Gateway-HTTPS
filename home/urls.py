from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('node_status', views.node_status, name='node_status'),
]