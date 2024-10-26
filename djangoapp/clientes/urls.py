from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.ClientesListView.as_view(), name='client_list'),
    path('add_cliente/', views.add_cliente, name='add_cliente'),
    path('clientes/detalhes/<int:cliente_id>/<str:tipo_cliente>/', views.detalhes_cliente, name='detalhes_cliente'),

]
