async function buscarDadosCNPJ(cnpj) {
    const url = `https://publica.cnpj.ws/cnpj/${cnpj}`;
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Erro ao buscar dados: ${response.statusText}`);
        }

        const dados = await response.json();
        return dados;
    } catch (error) {
        console.error('Erro:', error);
        return null;
    }
}

// Função para ser chamada quando o campo de CNPJ perder o foco (evento blur)
function configurarCampoCNPJ(idCampoCnpj, callback) {
    const campoCnpj = document.getElementById(idCampoCnpj);

    if (campoCnpj) {
        campoCnpj.addEventListener('blur', async function () {
            const cnpj = campoCnpj.value.replace(/\D/g, ''); // Remove caracteres não numéricos
            if (cnpj.length === 14) {
                const dadosCnpj = await buscarDadosCNPJ(cnpj);
                if (dadosCnpj) {
                    callback(dadosCnpj);
                } else {
                    console.error('Nenhum dado retornado da API.');
                }
            } else {
                console.error('CNPJ inválido.');
            }
        });
    }
}
