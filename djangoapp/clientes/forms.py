from django import forms
from django.core.exceptions import ValidationError
from .models import PessoaFisica, PessoaJuridica
from validate_docbr import CPF, CNPJ
import re
from django.db import IntegrityError

class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = ['nome', 'cpf_cnpj', 'contato', 'email', 'cep', 'logradouro', 'numero',
                'complemento', 'bairro', 'cidade', 'uf', 'rg', 'data_nascimento', 'observacoes', 'documentos']

        error_messages = {
            'nome': {
                'required': "O nome é obrigatório.",
                'max_length': "O nome não pode ter mais do que 100 caracteres."
            },
            'email': {
                'required': "O campo email é obrigatório.",
                'invalid': "Insira um email válido."
            },
            'cpf_cnpj': {
                'required': "CPF é obrigatório.",
                'invalid': "Insira um CPF válido."
            },
            'contato': {
                'required': "O número de contato é obrigatório.",
                'invalid': "Insira um número de contato válido."
            },
            'cep': {
                'required': "O CEP é obrigatório.",
                'invalid': "Insira um CEP válido."
            },
        }

    def clean_documentos(self):
        documento = self.cleaned_data.get('documentos', False)
        if documento:
            if documento.size > 5 * 1024 * 1024:  # Limite de 5MB
                raise ValidationError("O arquivo não pode ter mais de 5MB.")
            return documento
        return None  # Se o documento não foi anexado


    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data['cpf_cnpj']
        cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)  # Remove tudo que não for dígito

        if len(cpf_cnpj) == 11:
            cpf_validator = CPF()
            if not cpf_validator.validate(cpf_cnpj):
                raise ValidationError("O CPF informado é inválido.")
        elif len(cpf_cnpj) == 14:
            cnpj_validator = CNPJ()
            if not cnpj_validator.validate(cpf_cnpj):
                raise ValidationError("O CNPJ informado é inválido.")
        else:
            raise ValidationError("CPF ou CNPJ inválido.")

        return cpf_cnpj

    def clean_contato(self):
        contato = self.cleaned_data['contato']
        contato = re.sub(r'\D', '', contato)  # Remove todos os caracteres que não são números

        if len(contato) not in [10, 11]:
            raise ValidationError("O número de contato deve ter 10 ou 11 dígitos.")
        return contato

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        cep = re.sub(r'\D', '', cep)  # Remove todos os caracteres que não são números

        if len(cep) != 8:
            raise ValidationError("O CEP deve conter 8 dígitos.")
        return cep

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except IntegrityError as e:
            if 'unico_cpf_por_empresa' in str(e):
                raise forms.ValidationError("Já existe um cliente com este CPF cadastrado.")
            raise e


class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = ['nome', 'cpf_cnpj', 'contato', 'email', 'cep', 'logradouro', 'numero',
                'complemento', 'bairro', 'cidade', 'uf', 'razao_social', 'inscricao_estadual', 'observacoes', 'documentos']

        error_messages = {
            'nome': {
                'required': "O nome fantasia é obrigatório.",
                'max_length': "O nome não pode ter mais do que 100 caracteres."
            },
            'email': {
                'required': "O campo email é obrigatório.",
                'invalid': "Insira um email válido."
            },
            'cpf_cnpj': {
                'required': "CNPJ é obrigatório.",
                'invalid': "Insira um CNPJ válido."
            },
            'contato': {
                'required': "O número de contato é obrigatório.",
                'invalid': "Insira um número de contato válido."
            },
            'cep': {
                'required': "O CEP é obrigatório.",
                'invalid': "Insira um CEP válido."
            },
            'cpf_cnpj': {
                'required': "CPF ou CNPJ é obrigatório.",
                'invalid': "Insira um CPF ou CNPJ válido.",
                'unique': "Já existe um cadastro com este CPF/CNPJ." 
            },
        }

    def clean_documentos(self):
        documento = self.cleaned_data.get('documentos', False)
        if documento:
            if documento.size > 5 * 1024 * 1024:  # Limite de 5MB
                raise ValidationError("O arquivo não pode ter mais de 5MB.")
            return documento
        return None  # Se o documento não foi anexado


    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data['cpf_cnpj']
        cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)  # Remove tudo que não for dígito

        if len(cpf_cnpj) == 14:
            cnpj_validator = CNPJ()
            if not cnpj_validator.validate(cpf_cnpj):
                raise ValidationError("O CNPJ informado é inválido.")
        else:
            raise ValidationError("CNPJ inválido.")

        return cpf_cnpj

    def clean_contato(self):
        contato = self.cleaned_data['contato']
        contato = re.sub(r'\D', '', contato)  # Remove todos os caracteres que não são números

        if len(contato) not in [10, 11]:
            raise ValidationError("O número de contato deve ter 10 ou 11 dígitos.")
        return contato

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        cep = re.sub(r'\D', '', cep)  # Remove todos os caracteres que não são números

        if len(cep) != 8:
            raise ValidationError("O CEP deve conter 8 dígitos.")
        return cep

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except IntegrityError as e:
            if 'unico_cnpj_por_empresa' in str(e):
                raise forms.ValidationError("Já existe um cliente com este CNPJ cadastrado.")
            raise e