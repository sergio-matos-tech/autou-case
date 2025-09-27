import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError
# Importação de tipos do SDK da OpenAI para corrigir o aviso do Pylance
from openai.types.chat import ChatCompletionMessageParam
# Importações Pydantic para validação de esquema
from pydantic import BaseModel, Field, ValidationError 
from typing import Literal 

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- DEFINIÇÃO DO SCHEMA DE RESPOSTA (Pydantic) ---
class AnalysisResponse(BaseModel):
    """
    Define o esquema exato do JSON que esperamos da API da OpenAI.
    """
    category: Literal["Produtivo", "Improdutivo"] = Field(
        ..., description="A classificação do email."
    )
    suggested_response: str = Field(
        ..., description="A resposta automática sugerida em português."
    )

# --- INICIALIZAÇÃO DO CLIENTE OPENAI ---
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("A chave OPENAI_API_KEY não foi encontrada no arquivo .env")

    client = OpenAI(api_key=api_key)
    logging.info("Cliente OpenAI inicializado com sucesso.")

except Exception as e:
    logging.error(f"Erro ao inicializar o cliente OpenAI: {e}")
    client = None


# --- FUNÇÃO PRINCIPAL DO SERVIÇO ---

def analyze_email(text: str) -> dict:
    """
    Usa a API da OpenAI para classificar um email e sugerir uma resposta.
    """
    if not client:
        return {
            "category": "Erro",
            "suggested_response": "O cliente OpenAI não foi inicializado corretamente. Verifique a chave de API."
        }

    # PROMPT FINAL: Focado em Ação Obrigatória e Resposta Externa
    prompt = f"""
    Analise o conteúdo do seguinte email e retorne um objeto JSON com duas chaves:
    1. "category": classifique o email estritamente como "Produtivo" ou "Improdutivo", seguindo as regras abaixo:

    * Produtivo: Emails que exigem uma **ação obrigatória**, **resposta específica** ou **mudança de status** para avançar um processo de negócio (ex: solicitações de suporte, aprovações, dúvidas sobre o sistema, status de ticket, requisições de credenciais).
    * Improdutivo: Emails que **não necessitam de ação** ou **resposta imediata**. Inclui: mensagens de cortesia, parabéns, agradecimentos simples, **compartilhamento de informações/artigos (FYI)** e spam.

    2. "suggested_response":
    - Se o email for "Produtivo", sugira uma resposta curta, profissional e direcionada ao remetente original, indicando qual será o próximo passo da nossa equipe para resolver a questão. Sempre assine como "Equipe AutoU" ou "Equipe de Suporte AutoU".
    - Se o email for "Improdutivo" (ex: parabéns, cortesia, FYI, agradecimento), responda de forma cordial e sucinta, informando que não é necessária ação adicional ou que a mensagem foi recebida, evitando agradecimentos extensos ou respostas desnecessárias. Sempre assine como "Equipe AutoU" ou "Equipe de Suporte AutoU".

    Email para análise:
    ---
    {text}
    ---
    """

    # SYSTEM ROLE CORRIGIDO: Assume o papel de assistente de comunicação com o CLIENTE
    messages_list: list[ChatCompletionMessageParam] = [
        {"role": "system",
         "content": "Você é um assistente eficiente que analisa emails e retorna respostas em formato JSON. Suas respostas sugeridas devem ser **formais, profissionais e sempre direcionadas ao remetente original**, comunicando os próximos passos de forma clara."},
        {"role": "user", "content": prompt}
    ]
    
    response_format_json = {"type": "json_object"}

    try:
        logging.info("Enviando requisição para a API da OpenAI...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_list,
            temperature=0.2,
            response_format=response_format_json  # type: ignore
        )

        json_string = response.choices[0].message.content
        
        # CORREÇÃO DE TIPAGEM: Garante que json_string não é None antes de validar com Pydantic
        if json_string is None:
             raise ValueError("A resposta da API da IA não retornou conteúdo.")
             
        # Validação Pydantic
        analysis_data = AnalysisResponse.model_validate_json(json_string) 
        logging.info("Resposta validada com sucesso via Pydantic.")

        return {
            "category": analysis_data.category,
            "suggested_response": analysis_data.suggested_response
        }

    # Tratamento de Exceções Específicas
    except RateLimitError:
        logging.error("Erro de Rate Limit.")
        return {
            "category": "Erro de Serviço",
            "suggested_response": "A API está sobrecarregada ou excedeu o limite de requisições. Tente novamente mais tarde."
        }
    except APIError as e:
        logging.error(f"Erro na API da OpenAI: {e}")
        return {
            "category": "Erro de Serviço",
            "suggested_response": "Erro de autenticação ou configuração na API de IA. Contate o suporte técnico."
        }
    except (ValidationError, json.JSONDecodeError, ValueError) as e:
        logging.error(f"Erro de validação Pydantic ou JSON: {e}")
        return {
            "category": "Erro Inesperado",
            "suggested_response": "A IA não conseguiu retornar uma resposta no formato esperado. Tente refinar o email de entrada."
        }
    except Exception as e:
        logging.error(f"Erro inesperado durante a análise: {e}")
        return {
            "category": "Erro Inesperado",
            "suggested_response": "Ocorreu um erro inesperado ao analisar o email. Verifique o log para detalhes."
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
