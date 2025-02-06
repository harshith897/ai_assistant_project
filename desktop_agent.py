# desktop_agent.py
import speech_recognition as sr
import pyttsx3
import spacy
import requests
import platform
import subprocess
import time

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Server URL (adjust IP if your server is on a different machine)
SERVER_URL = "http://127.0.0.1:5000"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I could not understand that.")
    except sr.RequestError as e:
        speak("Could not request results; check your network connection.")
    return ""

def analyze_command(text):
    """Very basic intent detection using keyword matching."""
    text_lower = text.lower()
    if "remind" in text_lower:
        return "reminder"
    elif "open" in text_lower:
        return "open_app"
    else:
        return "general"

def execute_command(intent, text):
    if intent == "reminder":
        # Send a reminder to the server (assumes text after the word 'remind')
        reminder = text.partition("remind")[2].strip()
        if reminder:
            response = requests.post(f"{SERVER_URL}/add_reminder", json={"reminder": reminder})
            if response.ok:
                speak("Reminder added.")
            else:
                speak("Failed to add reminder.")
        else:
            speak("Please specify a reminder.")
    elif intent == "open_app":
        # Extract app name (naively, word after 'open')
        parts = text.split()
        try:
            app_index = parts.index("open")
            app_name = parts[app_index+1]
        except (ValueError, IndexError):
            app_name = ""
        if app_name:
            speak(f"Opening {app_name}.")
            open_application(app_name)
        else:
            speak("Please specify an application to open.")
    else:
        # For general commands, simply forward to the server
        response = requests.post(f"{SERVER_URL}/command", json={"command": text})
        if response.ok:
            speak("Command sent to the server.")
        else:
            speak("There was an error sending your command.")

def open_application(app_name):
    """Open an application based on your OS. This is a simplified example."""
    try:
        if platform.system() == "Windows":
            # For Windows, you may need to customize the command.
            subprocess.Popen(["start", app_name], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        else:  # Linux (assuming the app is in PATH)
            subprocess.Popen([app_name])
    except Exception as e:
        speak(f"Could not open {app_name}. Error: {e}")

def main_loop():
    speak("Desktop assistant started. Awaiting your command.")
    while True:
        command_text = listen_command()
        if command_text:
            intent = analyze_command(command_text)
            execute_command(intent, command_text)
        # Pause briefly between commands
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
