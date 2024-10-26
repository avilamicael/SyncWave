from django.db import models
from django.contrib.auth.models import AbstractUser

class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True)
    inscricao_estadual = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome_fantasia  


class Usuario(AbstractUser):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    is_trial = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Se não for superusuário, exigir que empresa seja preenchida
        if not self.is_superuser and not self.empresa:
            raise ValueError("Usuários comuns devem estar vinculados a uma empresa.")
        super(Usuario, self).save(*args, **kwargs)
