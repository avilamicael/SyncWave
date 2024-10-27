from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
import json, os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote

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

@login_required
def protected_media(request, path):
    # Decodifica o caminho para lidar com espaços e caracteres especiais
    path = unquote(path)
    # Constrói o caminho completo do arquivo
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        response = HttpResponse()
        response['Content-Type'] = ''  # O Nginx determinará o tipo de conteúdo
        # Define o cabeçalho X-Accel-Redirect com o caminho correto relativo ao Nginx
        response['X-Accel-Redirect'] = f'/protected_media/{path}'
        return response
    else:
        raise Http404
