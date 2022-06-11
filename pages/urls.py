from django.urls import path
from django.views.generic import TemplateView
from .views import buscarCliente, copiarFatura, imprimirFatura, listarFaturas

app_name = 'pages'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('buscar-cliente/', buscarCliente, name="bucarcliente"),
    path('fatura/<int:codFatura>', imprimirFatura, name="imprimirfatura"),
    path('digitavel-fatura/<int:codFatura>', copiarFatura, name="copiarfatura"),
    path('lista-de-fatura/<int:CodigoPessoa>', listarFaturas, name="listarfaturas"),
    
]
