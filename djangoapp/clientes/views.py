from django.views.generic import ListView
from itertools import chain
from django.db.models import Value, CharField
from .models import PessoaFisica, PessoaJuridica
from django.http import JsonResponse
from .forms import PessoaFisicaForm, PessoaJuridicaForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


# @method_decorator(login_required, name='dispatch')
class ClientesListView(ListView):
    template_name = 'frontend/clientes/client_list.html'
    context_object_name = 'clientes'
    
    def get_queryset(self):
        empresa = self.request.user.empresa

        pessoas_fisicas = PessoaFisica.objects.filter(empresa=empresa).values(
            'id', 'nome', 'cpf_cnpj', 'contato', 'logradouro', 'bairro', 'cidade', 'uf', 'data_cadastro', 'email', 'observacoes'
        ).annotate(cliente_tipo=Value('fisica', output_field=CharField()))

        pessoas_juridicas = PessoaJuridica.objects.filter(empresa=empresa).values(
            'id', 'nome', 'cpf_cnpj', 'contato', 'logradouro', 'bairro', 'cidade', 'uf', 'data_cadastro', 'email', 'observacoes'
        ).annotate(cliente_tipo=Value('juridica', output_field=CharField()))

        clientes = list(chain(pessoas_fisicas, pessoas_juridicas))
        
        return clientes

# @login_required
def add_cliente(request):
    if request.method == 'POST':
        cliente_tipo = request.POST.get('cliente_tipo')
        
        # Verificar qual formulário usar com base no tipo de cliente
        if cliente_tipo == 'fisica':
            form = PessoaFisicaForm(request.POST, request.FILES)
        else:
            form = PessoaJuridicaForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            try:
                # Salvar o cliente sem enviar ao banco (commit=False)
                cliente = form.save(commit=False)
                
                # Verifique se o usuário tem uma empresa associada
                if not hasattr(request.user, 'empresa') or request.user.empresa is None:
                    return JsonResponse({'success': False, 'errors': 'Usuário não tem uma empresa associada.'}, status=400)

                # Atribuir a empresa ao cliente
                cliente.empresa = request.user.empresa
                
                # Converter todos os campos de texto para maiúsculas, exceto campos de arquivo e campos relacionados a empresa
                for field, value in form.cleaned_data.items():
                    if isinstance(value, str):  # Apenas para campos de texto
                        setattr(cliente, field, value.upper())
                    else:
                        setattr(cliente, field, value)

                # Salvar o cliente no banco de dados
                cliente.save()

                # Se precisar salvar arquivos adicionais (dependendo da sua lógica)
                form.save_m2m()  # Para ManyToMany, se houver

                return JsonResponse({'success': True}, json_dumps_params={'ensure_ascii': False})
            
            except IntegrityError as e:
                # Verificar se o erro está relacionado ao CPF/CNPJ duplicado
                if 'unico_cpf_por_empresa' in str(e) or 'unico_cnpj_por_empresa' in str(e) or 'duplicate key' in str(e):
                    return JsonResponse({'success': False, 'errors': 'Já existe um cliente com este CPF/CNPJ cadastrado.'}, status=400)
                return JsonResponse({'success': False, 'errors': 'Erro de integridade ao salvar o cliente.'}, status=500)
            
            except ValidationError as e:
                return JsonResponse({'success': False, 'errors': e.message_dict}, status=400)

        # Retornar erros de validação do formulário
        return JsonResponse({'success': False, 'errors': form.errors}, status=400, json_dumps_params={'ensure_ascii': False})

    return JsonResponse({'success': False, 'message': 'Método de requisição inválido.'}, status=405, json_dumps_params={'ensure_ascii': False})

def detalhes_cliente(request, cliente_id, tipo_cliente):
    if tipo_cliente == 'fisica':
        cliente = get_object_or_404(PessoaFisica, id=cliente_id)
        dados_cliente = {
            'tipo': 'fisica',
            'cpf_cnpj': cliente.cpf_cnpj,
            'nome': cliente.nome,
            'email': cliente.email,
            'contato': cliente.contato,
            'cep': cliente.cep,
            'logradouro': cliente.logradouro,
            'numero': cliente.numero,
            'complemento': cliente.complemento,
            'bairro': cliente.bairro,
            'uf': cliente.uf,
            'cidade': cliente.cidade,
            'observacoes': cliente.observacoes,
            'rg': cliente.rg,
            'data_nascimento': cliente.data_nascimento,
            'documentos': cliente.documentos.url if cliente.documentos else None 

        }
    else:  # Pessoa Jurídica
        cliente = get_object_or_404(PessoaJuridica, id=cliente_id)
        dados_cliente = {
            'tipo': 'juridica',
            'cpf_cnpj': cliente.cpf_cnpj,
            'razao_social': cliente.razao_social,
            'inscricao_estadual': cliente.inscricao_estadual,
            'nome': cliente.nome,  # Nome fantasia
            'email': cliente.email,
            'contato': cliente.contato,
            'cep': cliente.cep,
            'logradouro': cliente.logradouro,
            'numero': cliente.numero,
            'complemento': cliente.complemento,
            'bairro': cliente.bairro,
            'uf': cliente.uf,
            'cidade': cliente.cidade,
            'observacoes': cliente.observacoes,
            'documentos': cliente.documentos.url if cliente.documentos else None  
        }

    # Retorna os dados do cliente em formato JSON
    return JsonResponse(dados_cliente)
