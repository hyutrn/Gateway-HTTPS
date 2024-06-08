from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login),
    re_path('login_page', views.login_page),
    re_path('test_token', views.test_token),
    re_path('sign_out', views.sign_out),
    path('chat/', include('chat.urls')),
    path('', include('nodes.urls')),
    path('', include('home.urls')),
    path('admin', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.STATIC_URL_MQTT, document_root=settings.STATIC_ROOT_MQTT)