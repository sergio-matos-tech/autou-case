import os
from flask import Flask, request, jsonify, render_template
from app.services.email_analyzer import analyze_email
import fitz  # A biblioteca PyMuPDF é importada como 'fitz'

app = Flask(__name__)

# Permite nomes de arquivo com extensões .txt e .pdf
ALLOWED_EXTENSIONS = {'txt', 'pdf'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    email_text = ""

    # 1. Prioriza o arquivo se ele for enviado
    if 'email_file' in request.files:
        file = request.files['email_file']

        if file and file.filename != '' and allowed_file(file.filename):
            try:
                if file.filename.lower().endswith('.pdf'):
                    # Processa o PDF
                    doc = fitz.open(stream=file.read(), filetype="pdf")
                    for page in doc:
                        email_text += page.get_text()
                    doc.close()
                elif file.filename.lower().endswith('.txt'):
                    # Processa o TXT
                    email_text = file.read().decode('utf-8')
            except Exception as e:
                return jsonify({"error": f"Erro ao ler o arquivo: {e}"}), 500

    # 2. Se nenhum arquivo válido foi processado, usa o texto do formulário
    if not email_text:
        # Para multipart/form-data, os dados de texto vêm em request.form
        email_text = request.form.get('email_text', '')

    # 3. Validação final
    if not email_text.strip():
        return jsonify({"error": "Nenhum arquivo válido ou texto foi fornecido."}), 400

    # 4. Chama o serviço de IA
    try:
        analysis_result = analyze_email(email_text)
        return jsonify(analysis_result), 200
    except Exception as e:
        return jsonify({"error": "Ocorreu um erro interno ao processar a solicitação."}), 500


if __name__ == '__main__':
    app.run(debug=True)