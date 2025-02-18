import google.generativeai as genai
import os
from dotenv import load_dotenv  # Certifique-se de instalar: pip install python-dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API do arquivo .env
api_key = os.getenv('Chave_API')

# Verifica se a chave da API está definida
if not api_key:
    print("Erro: Chave da API não encontrada. Verifique seu arquivo .env.")
    exit()

# Configura a API do Gemini
genai.configure(api_key=api_key)

# Lista os modelos disponíveis e seleciona um compatível
model_name = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print("Modelo disponível:", m.name)
        model_name = m.name

# Se nenhum modelo foi encontrado, encerra o programa
if not model_name:
    print("Erro: Nenhum modelo compatível encontrado.")
    exit()

# Inicializa o modelo
model = genai.GenerativeModel(model_name)

# Inicia a conversa
chat = model.start_chat(history=[])

# Mensagem de boas-vindas
bem_vindo = "# Bem-Vindo ao Assistente do NIA #"
print(len(bem_vindo) * "#")
print(bem_vindo)
print(len(bem_vindo) * "#")
print("### Digite 'sair' para encerrar ###\n")

# Loop principal do assistente
while True:
    texto = input("Você: ")

    if texto.lower() == "sair":
        print("Encerrando o chat...")
        break

    try:
        response = chat.send_message(texto)
        print("Gemini:", response.text, "\n")
    except Exception as e:
        print("Erro ao processar a mensagem:", e)

print("Chat encerrado.")

