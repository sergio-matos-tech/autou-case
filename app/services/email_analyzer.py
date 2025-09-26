import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Configuração básica para vermos informações úteis no terminal
logging.basicConfig(level=logging.INFO)

# Carrega as variáveis de ambiente (nossa chave de API) do arquivo .env
load_dotenv()

# --- INICIALIZAÇÃO DO MODELO GEMINI ---
try:
    # Pega a chave da API das variáveis de ambiente
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("A chave GOOGLE_API_KEY não foi encontrada no arquivo .env")

    # Configura a chave de API para a biblioteca
    genai.configure(api_key=api_key)
    
    # Configurações de geração para garantir uma saída JSON e ser mais direto
    generation_config = {
        "temperature": 0.2,
        "response_mime_type": "application/json",
    }

    # Inicializa o modelo. Usamos o 'gemini-1.5-pro-latest' já que você tem o plano Pro.
    # Ele é mais poderoso e sempre aponta para a versão mais recente.
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash-latest",
        generation_config=generation_config
    )
    logging.info("Modelo Gemini 1.5 Pro inicializado com sucesso.")

except Exception as e:
    logging.error(f"Erro ao inicializar o modelo Gemini: {e}")
    model = None

# --- FUNÇÃO PRINCIPAL DO SERVIÇO ---

def analyze_email(text: str) -> dict:
    """
    Usa a API do Google Gemini para classificar um email e sugerir uma resposta.

    Args:
        text: O conteúdo do email a ser analisado.

    Returns:
        Um dicionário contendo a categoria e a resposta sugerida.
    """
    if not model:
        return {
            "category": "Erro",
            "suggested_response": "O modelo Gemini não foi inicializado corretamente. Verifique a chave de API."
        }

    # O "prompt" é a nossa instrução detalhada para a IA.
    prompt = f"""
    Analise o conteúdo do seguinte email e retorne um objeto JSON com duas chaves:
    1. "category": classifique o email como "Produtivo" ou "Improdutivo". Emails que exigem uma ação, resposta ou contêm informações importantes são produtivos. E-mails de cortesia, agradecimentos simples ou spam são improdutivos.
    2. "suggested_response": sugira uma resposta curta e profissional em português, apropriada para a categoria.

    Email para análise:
    ---
    {text}
    ---
    """

    try:
        logging.info("Enviando requisição para a API do Gemini...")
        response = model.generate_content(prompt)

        # A API garante que a resposta.text será uma string JSON válida
        json_response = json.loads(response.text)
        logging.info("Resposta recebida e processada com sucesso.")

        return {
            "category": json_response.get("category", "Indeterminado"),
            "suggested_response": json_response.get("suggested_response", "Nenhuma sugestão gerada.")
        }

    except Exception as e:
        logging.error(f"Erro ao chamar a API do Gemini: {e}")
        return {
            "category": "Erro",
            "suggested_response": "Houve um problema ao se comunicar com a API. Tente novamente."
        }

# --- BLOCO DE TESTE ISOLADO ---
# Permite rodar este arquivo diretamente para verificar se a lógica funciona
if __name__ == '__main__':
    print("\n--- INICIANDO TESTE DO SERVIÇO DE ANÁLISE (Gemini Pro) ---")

    email_produtivo = "Olá, prezados. Gostaria de saber se há alguma atualização sobre o ticket de suporte #54321. O problema com o login ainda persiste. Agradeço a atenção."
    email_improdutivo = "Oi pessoal, só passando para desejar um ótimo final de semana a todos!"
    
    print("\n[TESTE 1: Email Produtivo]")
    analise1 = analyze_email(email_produtivo)
    print(f"Categoria: {analise1['category']}")
    print(f"Resposta Sugerida: {analise1['suggested_response']}")

    print("\n[TESTE 2: Email Improdutivo]")
    analise2 = analyze_email(email_improdutivo)
    print(f"Categoria: {analise2['category']}")
    print(f"Resposta Sugerida: {analise2['suggested_response']}")
