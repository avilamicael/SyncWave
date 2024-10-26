function mostrarNotificacao(mensagem, tipo = 'success') {
    const notificationContainer = document.getElementById('notification-container');
    
    // Criar o elemento da notificação
    const notification = document.createElement('div');
    notification.classList.add('notification', `notification-${tipo}`);

    // Ícones diferentes para cada tipo de notificação
    let iconClass = 'bx bx-bell';  // Ícone padrão
    if (tipo === 'success') {
        iconClass = 'bx bx-check-circle';
    } else if (tipo === 'error') {
        iconClass = 'bx bx-x-circle';
    } else if (tipo === 'info') {
        iconClass = 'bx bx-info-circle';
    } else if (tipo === 'warning') {
        iconClass = 'bx bx-error';
    }

    // Verificação para tratar mensagens complexas (como objetos com erros de formulário)
    let mensagemFormatada = '';

    if (typeof mensagem === 'object' && mensagem !== null) {
        for (let campo in mensagem) {
            if (mensagem.hasOwnProperty(campo)) {
                let mensagensCampo = mensagem[campo].join(', ');
                mensagemFormatada += `<strong>${campo.replace(/_/g, ' ')}:</strong> ${mensagensCampo}<br>`;
            }
        }
    } else {
        mensagemFormatada = mensagem;
    }

    // Ícone e Mensagem
    notification.innerHTML = `
        <i class="${iconClass} icon-bell"></i>
        <span class="message">${mensagemFormatada}</span>
        <button class="close-btn">&times;</button>
    `;

    // Adicionar notificação ao contêiner
    notificationContainer.appendChild(notification);

    // Adicionar a classe "show" para o fade-in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Remover a notificação após um tempo ou ao clicar no botão de fechar
    const removeNotification = () => {
        notification.classList.add('fadeout');
        setTimeout(() => {
            notification.remove();
        }, 500);
    };

    // Timeout para fadeout automático
    setTimeout(removeNotification, 5000);

    // Botão de fechar manualmente
    notification.querySelector('.close-btn').addEventListener('click', removeNotification);
}
