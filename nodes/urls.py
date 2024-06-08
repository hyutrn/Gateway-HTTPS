from django.urls import path
from . import views

urlpatterns = [
    path('register_node', views.register_node, name='register_node'),
    path('get_data', views.get_data, name='get_data'),
    path('auto_mode', views.auto_mode, name='auto_mode'),
]