import google.generativeai as genai
import os
from dotenv import load_dotenv

def main():
    assistente_falante = True
    ligar_microfone = True

    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configura a API do Gemini
    genai.configure(api_key=os.getenv('Chave_API'))

    # Lista os modelos disponíveis e seleciona um que suporta geração de conteúdo
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    # Configura a voz do assistente
    if assistente_falante:
        import pyttsx3
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('rate', 180)  # velocidade 120 = lento

        print("\nLista de Vozes - Verifique o número\n")
        for indice, vozes in enumerate(voices):  # listar vozes
            print(indice, vozes.name)

        voz = 1  # Escolha a voz desejada
        engine.setProperty('voice', voices[voz].id)

    # Configura o microfone
    if ligar_microfone:
        import speech_recognition as sr  # pip install SpeechRecognition
        r = sr.Recognizer()
        mic = sr.Microphone()

    # Mensagem de boas-vindas
    bem_vindo = "# Bem Vindo ao Assistente Mil Grau com Gemini AI #"
    print("")
    print(len(bem_vindo) * "#")
    print(bem_vindo)
    print(len(bem_vindo) * "#")
    print("###   Digite 'desligar' para encerrar    ###")
    print("")

    # Loop principal do assistente
    while True:
        if ligar_microfone:
            with mic as fonte:
                r.adjust_for_ambient_noise(fonte)
                print("Fale alguma coisa (ou diga 'desligar')")
                audio = r.listen(fonte)
                print("Enviando para reconhecimento")
                try:
                    texto = r.recognize_google(audio, language="pt-BR")
                    print("Você disse: {}".format(texto))
                except Exception as e:
                    print("Não entendi o que você disse. Erro:", e)
                    texto = ""
        else:
            texto = input("Escreva sua mensagem (ou 'desligar'): ")

        if texto.lower() == "desligar":
            break

        # Envia a mensagem para o Gemini e obtém a resposta
        response = chat.send_message(texto)
        print("Gemini:", response.text, "\n")

        # Fala a resposta do Gemini
        if assistente_falante:
            engine.say(response.text)
            engine.runAndWait()

    print("Encerrando Chat")

if __name__ == '__main__':
    main()