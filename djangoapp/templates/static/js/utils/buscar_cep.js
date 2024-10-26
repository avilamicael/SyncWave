async function buscarCEP(cep) {
    const cepLimpo = cep.replace(/\D/g, '');

    if (cepLimpo.length !== 8) {
        enviarMensagemDjango('CEP inválido!', 'error');
        return;
    }

    try {
        const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
        
        if (!response.ok) {
            throw new Error('Erro ao buscar CEP');
        }

        const dados = await response.json();

        if (dados.erro) {
            enviarMensagemDjango('CEP não encontrado!', 'error');
            return;
        }

        return dados;

    } catch (error) {
        enviarMensagemDjango(`Erro: ${error.message}`, 'error');
    }
}

// Função para enviar mensagens ao Django
function enviarMensagemDjango(mensagem, tipo) {
    fetch('/adicionar-mensagem/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            mensagem: mensagem,
            tipo: tipo
        })
    }).then(() => {
        mostrarNotificacao(mensagem, tipo);
    });
}
