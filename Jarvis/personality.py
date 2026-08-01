"""
personality.py
----------------
Jarvis's canned personality responses: greetings, small talk, and
self-introduction. Nothing here touches system state; each function
just picks one of a few pre-written lines and speaks it.
"""

import random
import datetime
from speech import speak


def randomgen(n):
    '''Generates a random number from 1 to n.'''
    return random.randint(1, n)

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning sir")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon sir")
    else:
        speak("Good Evening sir")
    x = randomgen(3)
    if x == 1:
        speak('What can I do for you today ?')
    elif x == 2:
        speak("How can I help you today ?")
    elif x == 3:
        speak("How may I help you today ?")

def introduce():
    '''Introduces itself to the user.'''
    x = randomgen(15)
    if x == 1:
        speak("Hello, I'm Jarvis, your virtual assistant!")
    elif x == 2:
        speak("Hi there, I'm Jarvis, nice to meet you.")
    elif x == 3:
        speak("Greetings! My name is Jarvis and I'm here to assist you.")
    elif x == 4:
        speak("Hello! My name is Jarvis and I'm an AI assistant created to be helpful, harmless, and honest.")
    elif x == 5:
        speak("Hi, I'm Jarvis! I'm an AI designed to provide helpful information.")
    elif x == 6:
        speak("Hello, my name is Jarvis. I'm an AI assistant ready to answer your questions and provide information.")
    elif x == 7:
        speak("Greetings, I'm Jarvis! I'm an artificial intelligence created by Anthropic to be helpful, harmless, and honest.")
    elif x == 8:
        speak("Hi there! I'm Jarvis, your new AI assistant. How can I help you today?")
    elif x == 9:
        speak("Hello, I'm Jarvis! I'm an AI assistant created by Anthropic to be helpful, harmless, and honest.")
    elif x == 10:
        speak("Greetings, my name is Jarvis. I'm an AI assistant created to provide helpful information to you.")
    elif x == 11:
        speak("My name is jarvis and I was created by Avaneesh R and I am programmed to be your desktop voice assistant. I will try to help you in the best way I can")
    elif x == 12:
        speak("I am jarvis and I am a desktop assistant. You can ask me to perform certain tasks for you.")
    elif x == 13:
        speak("I am a desktop assistant and my name is jarvis. I can lend you a hand in various tasks that you do everytime on the computer.")
    elif x == 14:
        speak("My name is Jarvis and I am your desktop assistant. Feel free to ask me anything you like.")
    else:
        speak("My name is jarvis and I am your personal desktop assistant. If you need anything just let me know.")
