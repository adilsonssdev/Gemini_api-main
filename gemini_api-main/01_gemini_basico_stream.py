import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API
api_key = os.getenv('Chave_API')

# Verifica se a chave da API foi carregada corretamente
if not api_key:
    print("Erro: Chave da API não encontrada. Verifique o arquivo .env.")
    exit()

# Configura a API com a chave
genai.configure(api_key=api_key)

try:
    # Lista modelos disponíveis
    modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

    # Seleciona o modelo preferido (Gemini 2.0 Pro, se disponível)
    modelo_preferido = next((m for m in modelos_disponiveis if "gemini-2" in m), None)

    if not modelo_preferido:
        modelo_preferido = next((m for m in modelos_disponiveis if "gemini-1.5" in m), None)

    if not modelo_preferido:
        print("Nenhum modelo Gemini Pro atualizado disponível. Verifique sua conta.")
        exit()

    print(f"Usando modelo: {modelo_preferido}")

    # Inicializa o modelo
    model = genai.GenerativeModel(modelo_preferido)

    # Faz a requisição ao Gemini
    response = model.generate_content("Fale me sobre UiPath")

    print("\nResposta do Gemini:\n")
    print(response.text if response else "Resposta vazia.")

except Exception as e:
    print(f"Erro ao conectar à API: {e}")

