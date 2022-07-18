from venv import create
from django.db import models

# Create your models here.
class Solicitacoes(models.Model):
    cod_cliente = models.CharField(max_length=50, verbose_name="Código do Cliente", blank=False)
    venc_Fatura = models.CharField(max_length=50, verbose_name="Vencimento da Fatura", blank=False)
    imprimiu = models.BooleanField(default=False)
    copiou = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.cod_cliente