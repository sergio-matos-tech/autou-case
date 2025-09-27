import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- INICIALIZAÇÃO DO CLIENTE OPENAI ---
try:
    # Pega a chave da API das variáveis de ambiente
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("A chave OPENAI_API_KEY não foi encontrada no arquivo .env")

    # Cria o cliente que usaremos para fazer as chamadas
    client = OpenAI(api_key=api_key)
    logging.info("Cliente OpenAI inicializado com sucesso.")

except Exception as e:
    logging.error(f"Erro ao inicializar o cliente OpenAI: {e}")
    client = None

# --- FUNÇÃO PRINCIPAL DO SERVIÇO ---

def analyze_email(text: str) -> dict:
    """
    Usa a API da OpenAI para classificar um email e sugerir uma resposta.

    Args:
        text: O conteúdo do email a ser analisado.

    Returns:
        Um dicionário contendo a categoria e a resposta sugerida.
    """
    if not client:
        return {
            "category": "Erro",
            "suggested_response": "O cliente OpenAI não foi inicializado corretamente. Verifique a chave de API."
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
        logging.info("Enviando requisição para a API da OpenAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo rápido e eficiente
            messages=[
                {"role": "system", "content": "Você é um assistente eficiente que analisa emails e retorna respostas em formato JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Baixa temperatura para respostas mais diretas
            response_format={"type": "json_object"} # Garante que a resposta será um JSON
        )
        
        json_response = json.loads(response.choices[0].message.content)
        logging.info("Resposta recebida e processada com sucesso.")
        
        return {
            "category": json_response.get("category", "Indeterminado"),
            "suggested_response": json_response.get("suggested_response", "Nenhuma sugestão gerada.")
        }

    except Exception as e:
        logging.error(f"Erro ao chamar a API da OpenAI: {e}")
        return {
            "category": "Erro",
            "suggested_response": "Houve um problema ao se comunicar com a API. Tente novamente."
        }

# --- BLOCO DE TESTE ISOLADO ---
if __name__ == '__main__':
    print("\n--- INICIANDO TESTE DO SERVIÇO DE ANÁLISE (OpenAI) ---")

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
