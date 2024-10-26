from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('adicionar-mensagem/', views.adicionar_mensagem, name='adicionar_mensagem'),
    path('protected_media/<path:path>/', views.protected_media, name='protected_media'),

    ]
