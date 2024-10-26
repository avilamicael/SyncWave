from django.db import models
from core.models import Empresa
from django.urls import reverse
from urllib.parse import quote  

class ClienteBase(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=18)
    contato = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    documentos = models.FileField(upload_to='documentos/cadastro/clientes/', blank=True, null=True)
    status = models.CharField(max_length=255, default='Ativo')
    
    class Meta:
        abstract = True

    @property
    def documentos_protegidos_url(self):
        """Retorna a URL protegida para o documento."""
        if self.documentos:
            # Garantir que o caminho esteja codificado corretamente usando urllib.parse.quote
            path = quote(self.documentos.name)
            # Gera a URL protegida usando o caminho armazenado no campo 'documentos'
            return reverse('protected_media', args=[path])
        return None


class PessoaFisica(ClienteBase):
    rg = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    @property
    def tipo_cliente(self):
        return 'fisica'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'cpf_cnpj'], name='unico_cpf_por_empresa')
        ]  # Nome da constraint ajustado para ser único

class PessoaJuridica(ClienteBase):
    razao_social = models.CharField(max_length=255)
    inscricao_estadual = models.CharField(max_length=15, blank=True, null=True)

    @property
    def tipo_cliente(self):
        return 'juridica'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'cpf_cnpj'], name='unico_cnpj_por_empresa')
        ]  # Nome da constraint ajustado para ser único
