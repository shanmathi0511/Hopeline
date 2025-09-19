import pyttsx3
import speech_recognition as sr

# Text to Speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Speech to Text
def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand that."
    except sr.RequestError:
        return "Sorry, speech service is unavailable."
