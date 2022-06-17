from django.urls import path
from django.views.generic import TemplateView
from .views import buscarCliente, copiarFatura, imprimirFatura, listarFaturasSF, listarFaturasCPS

app_name = 'pages'

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('buscar-cliente/', buscarCliente, name="bucarcliente"),
    path('fatura/<int:codFatura>', imprimirFatura, name="imprimirfatura"),
    path('digitavel-fatura/<int:codFatura>', copiarFatura, name="copiarfatura"),
    path('lista-de-fatura-SF/<int:CodigoPessoa>', listarFaturasSF, name="listarfaturasSF"),
    path('lista-de-fatura-cps/<int:CodigoPessoa>', listarFaturasCPS, name="listarfaturasCPS"),
    
]
