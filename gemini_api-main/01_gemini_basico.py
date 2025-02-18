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

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Qual o sentido da vida?")

print(response.text)
