# import google.generativeai as genai
# import PIL.Image

import google.generativeai as genai
import PIL.Image
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

# Verifica o diretório atual de execução
print("Diretório atual:", os.getcwd())

# Caminho relativo para a pasta IMG, dentro do diretório 'gemini_api-main'
script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório onde o script está
img_folder = os.path.join(script_dir, 'Img')  # Diretório correto para a pasta Img

# Verifica se a pasta IMG existe
if os.path.exists(img_folder):
    imagens = [f for f in os.listdir(img_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    if not imagens:
        print(f"Erro: Não há imagens na pasta '{img_folder}'.")
        exit()  # Encerra o script se não houver imagens
    print("Imagens encontradas na pasta:")
    for i, imagem in enumerate(imagens, 1):
        print(f"{i}. {imagem}")
else:
    print(f"Erro: A pasta '{img_folder}' não foi encontrada.")
    exit()  # Encerra o script se a pasta não for encontrada

# Função para processar a pergunta do usuário sobre a imagem
def processar_imagem(imagem_nome):
    # Caminho absoluto para a imagem
    img_path = os.path.join(img_folder, imagem_nome)

    # Verifica se a imagem existe
    if os.path.exists(img_path):
        img = PIL.Image.open(img_path)
    else:
        print(f"Erro: Arquivo '{img_path}' não encontrado.")
        return

    # Pergunta do usuário
    pergunta = input(f"Escolha a imagem '{imagem_nome}', descreva sua pergunta: ")

    # Criação do modelo com o modelo atualizado
    model = genai.GenerativeModel('gemini-1.5-flash')  # Novo modelo

    # Gerar a resposta para a pergunta
    try:
        response = model.generate_content([pergunta, img])
        response.resolve()
        print("Resposta da pergunta:", response.text)
    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")

# Fluxo de interação com o usuário
while True:
    # Solicitar ao usuário que escolha uma imagem
    escolha = input(f"Escolha a imagem (digite o número ou 'sair' para encerrar): ").strip().lower()

    if escolha == 'sair':
        print("Encerrando o chat.")
        break

    try:
        escolha_num = int(escolha)
        if 1 <= escolha_num <= len(imagens):
            imagem_escolhida = imagens[escolha_num - 1]
            processar_imagem(imagem_escolhida)
        else:
            print("Escolha inválida. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite o número correspondente à imagem ou 'sair' para encerrar.")

    # Perguntar se o usuário deseja escolher outra imagem
    continuar = input("Gostaria de verificar outra imagem? (sim/não): ").strip().lower()
    if continuar != 'sim':
        print("Encerrando o chat.")
        break
