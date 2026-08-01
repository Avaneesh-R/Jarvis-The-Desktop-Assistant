"""
speech.py
-----------
Voice I/O layer: text-to-speech output and speech-to-text input.
Every other module calls into this one rather than touching
pyttsx3 / speech_recognition directly.
"""

import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()


def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    '''Takes voice input from the microphone and returns it as text.'''
    global r
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold + 4
        audio = r.listen(source)
    done = 0
    while done == 0:
        try:
            print("Recognizing.....")
            query = r.recognize_google(audio, language="en-uk")
            print(f"User said: {query}\n")
            done = 1
        except:
            print("I was unable to understand. Please try again....")
            done = 0
            return "none123"
        return query
