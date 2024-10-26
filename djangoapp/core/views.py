from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
import json, os
from django.http import FileResponse, Http404
from django.conf import settings

def home(request):
    return render(request, 'frontend/home.html')

def adicionar_mensagem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mensagem = data.get('mensagem')
        tipo = data.get('tipo')

        if tipo == 'success':
            messages.success(request, mensagem)
        elif tipo == 'error':
            messages.error(request, mensagem)
        elif tipo == 'warning':
            messages.warning(request, mensagem)
        else:
            messages.info(request, mensagem)

        return JsonResponse({'status': 'Mensagem adicionada com sucesso'})
    return JsonResponse({'status': 'Método não permitido'}, status=405)

def protected_media(request, path):
    # Verifique se o usuário está autenticado
    if not request.user.is_authenticated:
        raise Http404("Você não tem permissão para acessar este arquivo.")

    # Caminho absoluto do arquivo no sistema de arquivos
    full_path = os.path.join(settings.MEDIA_ROOT, path)

    # Verificar se o arquivo existe no sistema de arquivos
    if not os.path.exists(full_path):
        raise Http404("Arquivo não encontrado.")

    # Servir o arquivo
    return FileResponse(open(full_path, 'rb'))
