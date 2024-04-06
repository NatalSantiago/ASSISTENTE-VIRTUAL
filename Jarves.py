import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import psutil
import subprocess

# Função para falar


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Função para ouvir o comando de voz


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = r.listen(source)

    try:
        print("Reconhecendo...")
        # Reconhece a fala em Português do Brasil
        query = r.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {query}\n")
        return query.lower()
    except Exception as e:
        print("Desculpe, não consegui entender. Poderia repetir?")
        return None

# Função para finalizar um aplicativo com base no nome da janela


def kill_process_by_window_name(window_name):
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name', 'username'])
            proc_pid = proc_info['pid']
            # Obter as janelas associadas ao processo usando o comando tasklist
            result = subprocess.check_output(
                f'tasklist /FI "PID eq {proc_pid}" /V /FO LIST', shell=True).decode('latin-1')
            if window_name.lower() in result.lower():
                proc.kill()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, subprocess.CalledProcessError):
            continue
    return False

# Função para abrir um aplicativo pelo nome


def open_application(app_name):
    try:
        subprocess.Popen(app_name)  # Tenta abrir o aplicativo pelo nome
        return True
    except Exception as e:
        print(f"Erro ao abrir {app_name}: {e}")
        return False

# Função principal do assistente


def jarves_assistant():
    speak("Bem-vindo, sou Jarves seu assistente pessoal. O que você deseja?")

    while True:
        command = listen()  # Obter o comando do usuário em texto

        if command:
            if 'abrir aplicativo' in command:
                speak("Qual aplicativo você deseja abrir?")
                app_name = listen().lower()
                if app_name:
                    if open_application(app_name):
                        speak(f"Aplicativo {app_name} aberto.")
                    else:
                        speak(
                            f"Não foi possível abrir o aplicativo {app_name}.")

            elif 'finalizar aplicativo' in command:
                speak("Qual aplicativo você deseja finalizar?")
                app_to_close = listen().lower()
                if app_to_close:
                    if kill_process_by_window_name(app_to_close):
                        speak(f"Aplicativo {app_to_close} finalizado.")
                    else:
                        speak(
                            f"Não foi possível encontrar o aplicativo {app_to_close}.")

            elif 'pesquisar na internet' in command:
                speak("O que você gostaria de pesquisar?")
                search_query = listen()
                if search_query:
                    url = f"https://www.google.com/search?q={search_query}"
                    webbrowser.open(url)
                    speak(f"Aqui estão os resultados para {search_query}")

            elif 'criar lembrete' in command:
                speak("Para criar um lembrete, qual é o lembrete?")
                reminder_text = listen()
                if reminder_text:
                    speak(f"Lembrete criado: {reminder_text}")
                    # Aqui você poderia adicionar a lógica para definir um lembrete

            elif 'finalizar assistente' in command or 'sair assistente' in command:
                speak("Até logo! Encerrando o assistente.")
                break

            else:
                speak("Desculpe, não entendi o comando. Poderia repetir?")

        else:
            speak("Desculpe, não consegui entender. Poderia repetir?")


# Chamada para iniciar o assistente
if __name__ == "__main__":
    jarves_assistant()
