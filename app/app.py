from flask import Flask, request, jsonify, render_template  # Adicione render_template
from app.services.email_analyzer import analyze_email

app = Flask(__name__)

@app.route('/')
def home():
    # Em vez de retornar uma string, agora renderizamos nosso arquivo HTML
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({"error": "O campo 'text' é obrigatório e não pode estar vazio."}), 400

    email_text = data['text']

    try:
        analysis_result = analyze_email(email_text)
        return jsonify(analysis_result), 200
    except Exception as e:
        return jsonify({"error": "Ocorreu um erro interno ao processar a solicitação."}), 500

# Este bloco não é mais necessário se usarmos 'flask run', mas não prejudica.
if __name__ == '__main__':
    app.run(debug=True)