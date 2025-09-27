document.addEventListener('DOMContentLoaded', () => {
    // --- Referências aos elementos da UI ---
    const inputSection = document.getElementById('input-section');
    const outputSection = document.getElementById('output-section');
    const form = document.getElementById('analysis-form');
    const emailTextInput = document.getElementById('email-text');
    const emailFileInput = document.getElementById('email-file');
    const fileDropArea = document.querySelector('.file-drop-area');
    const fileMsg = document.querySelector('.file-msg');
    const fileLoader = document.querySelector('.file-loader');
    const submitButton = document.getElementById('submit-button');
    const mainLoader = document.getElementById('loader');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    const resultsContainer = document.getElementById('results-container');
    const resultCategory = document.getElementById('result-category');
    const resultResponse = document.getElementById('result-response');
    const tryAgainButton = document.getElementById('try-again-button');
    const analyzeNewButton = document.getElementById('analyze-new-button');

    // --- Utilitários ---
    const showFileLoader = () => {
        fileMsg.classList.add('hidden');
        fileLoader.classList.remove('hidden'); // depende de .file-loader.hidden { display: none; } no CSS
    };
    const hideFileLoader = () => {
        fileLoader.classList.add('hidden');
        fileMsg.classList.remove('hidden');
    };

    // --- Funções de Controle da UI ---
    const resetFormToIdle = () => {
        inputSection.classList.remove('hidden');
        outputSection.classList.add('hidden');
        form.reset();
        emailTextInput.disabled = false;
        emailFileInput.disabled = false;
        fileDropArea.classList.remove('disabled');
        fileMsg.textContent = 'Arraste e solte o arquivo aqui, ou clique para selecionar';
        fileMsg.classList.remove('hidden');
        hideFileLoader();
        validateInput();
    };

    const validateInput = () => {
        const hasText = emailTextInput.value.trim().length > 0;
        const hasFile = emailFileInput.files.length > 0;
        submitButton.disabled = !hasText && !hasFile;
    };

    // --- Eventos ---
    emailTextInput.addEventListener('input', () => {
        if (emailTextInput.value.trim().length > 0) {
            // se o usuário digitou texto, limpamos o arquivo
            emailFileInput.value = '';
            emailFileInput.disabled = true;
            fileDropArea.classList.add('disabled');
            fileMsg.textContent = 'Arraste e solte o arquivo aqui, ou clique para selecionar';
            fileMsg.classList.remove('hidden');
            hideFileLoader();
        } else {
            emailFileInput.disabled = false;
            fileDropArea.classList.remove('disabled');
        }
        validateInput();
    });

    // Lê o arquivo com FileReader; mostra loader enquanto lê
    const readFileAndUpdateUI = (file) => {
        showFileLoader();

        const reader = new FileReader();
        let cleared = false;

        // fallback de segurança: se algo travar, garantimos que o loader seja escondido após 20s
        const fallback = setTimeout(() => {
            if (!cleared) {
                hideFileLoader();
                fileMsg.textContent = `Arquivo selecionado: ${file.name}`;
                fileMsg.classList.remove('hidden');
                validateInput();
                cleared = true;
            }
        }, 20000);

        reader.onerror = () => {
            hideFileLoader();
            fileMsg.textContent = `Erro ao ler o arquivo: ${file.name}`;
            fileMsg.classList.remove('hidden');
            emailFileInput.value = '';
            emailTextInput.disabled = false;
            fileDropArea.classList.remove('disabled');
            validateInput();
            cleared = true;
            clearTimeout(fallback);
        };

        reader.onload = () => {
            // leitura concluída com sucesso
            hideFileLoader();
            fileMsg.textContent = `Arquivo carregado: ${file.name}`;
            fileMsg.classList.remove('hidden');
            validateInput();
            cleared = true;
            clearTimeout(fallback);
        };

        reader.onloadend = () => {
            // redundância segura para garantir esconder o loader
            hideFileLoader();
            clearTimeout(fallback);
        };

        // iniciando leitura de acordo com extensão
        try {
            const isTxt = file.name.toLowerCase().endsWith('.txt');
            if (isTxt) reader.readAsText(file);
            else reader.readAsArrayBuffer(file); // pdf, etc.
        } catch (err) {
            // erro síncrono inesperado
            hideFileLoader();
            fileMsg.textContent = `Erro ao processar o arquivo: ${file.name}`;
            fileMsg.classList.remove('hidden');
            emailFileInput.value = '';
            emailTextInput.disabled = false;
            fileDropArea.classList.remove('disabled');
            validateInput();
            clearTimeout(fallback);
        }
    };

    // Handler change do input file
    emailFileInput.addEventListener('change', () => {
        const file = emailFileInput.files[0];

        if (file) {
            emailTextInput.value = '';
            emailTextInput.disabled = true;
            fileDropArea.classList.add('disabled');

            readFileAndUpdateUI(file);
        } else {
            // cancelou seleção
            emailTextInput.disabled = false;
            fileDropArea.classList.remove('disabled');
            hideFileLoader();
            validateInput();
        }
    });

    // Drag & drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev => {
        fileDropArea.addEventListener(ev, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });
    ['dragenter', 'dragover'].forEach(ev => {
        fileDropArea.addEventListener(ev, () => {
            if (!emailTextInput.disabled) fileDropArea.classList.add('highlight');
        });
    });
    ['dragleave', 'drop'].forEach(ev => {
        fileDropArea.addEventListener(ev, () => fileDropArea.classList.remove('highlight'));
    });

    fileDropArea.addEventListener('drop', e => {
        if (emailTextInput.disabled) return;
        const files = e.dataTransfer.files;
        if (!files || files.length === 0) return;
        emailFileInput.files = files;
        const ev = new Event('change', { bubbles: true });
        emailFileInput.dispatchEvent(ev);
    });

    // Submit do formulário
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        // garantir que o loader do arquivo não permaneça visível ao enviar
        hideFileLoader();

        inputSection.classList.add('hidden');
        outputSection.classList.remove('hidden');
        mainLoader.classList.remove('hidden');
        errorContainer.classList.add('hidden');
        resultsContainer.classList.add('hidden');
        submitButton.disabled = true;

        const formData = new FormData(form);

        try {
            const response = await fetch('/analyze', { method: 'POST', body: formData });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Ocorreu um erro desconhecido.');

            resultCategory.textContent = data.category;
            resultResponse.textContent = data.suggested_response;
            resultsContainer.classList.remove('hidden');
        } catch (error) {
            errorMessage.textContent = error.message;
            errorContainer.classList.remove('hidden');
        } finally {
            mainLoader.classList.add('hidden');
        }
    });

    // Botões de reset
    tryAgainButton.addEventListener('click', resetFormToIdle);
    analyzeNewButton.addEventListener('click', resetFormToIdle);

    // Inicializa
    resetFormToIdle();
});
