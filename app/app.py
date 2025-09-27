import os
import re  # Módulo adicionado para Expressões Regulares (NLP)
from flask import Flask, request, jsonify, render_template
from app.services.email_analyzer import analyze_email
import fitz  # A biblioteca PyMuPDF é importada como 'fitz'

app = Flask(__name__)

# Permite nomes de arquivo com extensões .txt e .pdf
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

@app.errorhandler(413)
def file_size_too_large(e):
    return jsonify({"error": "Arquivo muito grande. O tamanho máximo permitido é de 5 MB."}), 413

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_text(text: str) -> str:
    """
    Realiza pré-processamento clássico para padronizar o texto antes de enviar para a IA.
    1. Converte para minúsculas.
    2. Remove pontuações e caracteres especiais, mantendo letras, números e espaços.
    """
    # 1. Converte para minúsculas
    text = text.lower()
    # 2. Remove pontuações e caracteres especiais
    # Mantém apenas caracteres alfanuméricos e espaços
    text = re.sub(r'[^\w\s\n]', '', text)
    # 3. Normaliza espaços (remove múltiplos espaços) e retira bordas
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    email_text = ""

    # 1. Prioriza o arquivo se ele for enviado
    if 'email_file' in request.files:
        file = request.files['email_file']

        if file and file.filename and file.filename != '' and allowed_file(file.filename):
            try:
                filename_lower = file.filename.lower() if file.filename else ''
                if filename_lower.endswith('.pdf'):
                    # Processa o PDF usando PyMuPDF (fitz)
                    doc = fitz.open(stream=file.read(), filetype="pdf")
                    for page in doc:
                        # Garante que page é do tipo fitz.Page
                        if hasattr(page, 'get_text'):
                            email_text += page.get_text()  # type: ignore
                    doc.close()
                elif filename_lower.endswith('.txt'):
                    # Processa o TXT
                    email_text = file.read().decode('utf-8')
            except Exception as e:
                return jsonify({"error": f"Erro ao ler o arquivo: {e}"}), 500

    # 2. Se nenhum arquivo válido foi processado, usa o texto do formulário
    if not email_text:
        # CORREÇÃO: Usa 'email_text' que é o nome correto do campo no HTML
        email_text = request.form.get('email_text', '')

    # 3. Validação final
    if not email_text.strip():
        return jsonify({"error": "Nenhum arquivo válido ou texto foi fornecido."}), 400

    # 4. PRÉ-PROCESSAMENTO: Aplica as técnicas clássicas de NLP antes da IA
    processed_text = preprocess_text(email_text)

    # 5. Chama o serviço de IA
    try:
        # Passa o texto pré-processado
        analysis_result = analyze_email(processed_text)
        return jsonify(analysis_result), 200
    except Exception as e:
        # Erro interno na chamada da API de IA
        return jsonify({"error": "Ocorreu um erro interno ao processar a solicitação."}), 500


if __name__ == '__main__':
    # Teste rápido da função de pré-processamento
    test_text = "Subject: Urgent Issue! 1. The price is $100."
    print(f"Texto original: {test_text}")
    print(f"Texto processado: {preprocess_text(test_text)}")

    app.run(debug=True)
