// Aguarda o conteúdo da página carregar completamente
document.addEventListener('DOMContentLoaded', () => {

    // Pega as referências dos elementos HTML que vamos usar
    const form = document.getElementById('analysis-form');
    const emailText = document.getElementById('email-text');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const resultCategory = document.getElementById('result-category');
    const resultResponse = document.getElementById('result-response');

    // Adiciona um "ouvinte" para o evento de envio do formulário
    form.addEventListener('submit', async (event) => {
        // Impede o comportamento padrão do formulário (que é recarregar a página)
        event.preventDefault();

        const text = emailText.value;

        // Validação simples para não enviar texto vazio
        if (!text.trim()) {
            alert('Por favor, insira o texto de um email.');
            return;
        }

        // Prepara a interface para a chamada da API
        resultsContainer.classList.add('hidden'); // Esconde resultados antigos
        loader.classList.remove('hidden'); // Mostra o spinner de carregamento

        try {
            // Faz a chamada para a nossa API Flask usando 'fetch'
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Converte o objeto JavaScript em uma string JSON
                body: JSON.stringify({ text: text }),
            });

            // Pega a resposta JSON da API
            const data = await response.json();

            if (!response.ok) {
                // Se a API retornar um erro (ex: 400 ou 500), exibe o erro
                throw new Error(data.error || 'Ocorreu um erro na API.');
            }

            // Atualiza a página com os resultados recebidos
            resultCategory.textContent = data.category;
            resultResponse.textContent = data.suggested_response;

            // Mostra o contêiner de resultados
            resultsContainer.classList.remove('hidden');

        } catch (error) {
            // Em caso de erro de rede ou da API, mostra um alerta
            console.error('Erro ao analisar:', error);
            alert(`Erro ao processar a solicitação: ${error.message}`);
        } finally {
            // Garante que o spinner de carregamento sempre será escondido no final
            loader.classList.add('hidden');
        }
    });
});