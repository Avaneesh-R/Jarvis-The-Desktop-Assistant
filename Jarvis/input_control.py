"""
input_control.py
-------------------
Keyboard/typing helpers: simulating key presses, typing text on the
user's behalf, dictation ("typing mode"), and reading clipboard text
aloud.
"""

import pyautogui
import pyperclip

from speech import speak, takeCommand


def press(query):
    query = query.replace('control', 'ctrl')
    query = query.replace('windows', 'super')
    query = query.replace('window', 'super')
    query = query.replace('left arrow', 'left')
    query = query.replace('right arrow', 'right')
    query = query.replace('up arrow', 'up')
    query = query.replace('down arrow', 'down')
    query = query.replace('key', '')
    query = query.replace('keys', '')
    query = query.split(sep=' ')
    if len(query) == 1:
        pyautogui.press(f'{query[0]}')
    elif len(query) == 2:
        pyautogui.hotkey(f'{query[0]}', f'{query[1]}')


def Type(query):
    query = query.replace('jarvis', '')
    query = query.replace('javed', '')
    query = query.replace('type', '')
    pyautogui.typewrite(query, 0.07)


def typeAndEnter(query):
    query = query.replace('jarvis', '')
    query = query.replace('javed', '')
    query = query.replace('enter', '')
    query = query.replace('type', '')
    query = query.replace('type and enter', '')
    Type(query)
    press('enter')


def typingMode():
    speak('Start now')
    while True:
        query = takeCommand()
        query_l = query.lower()
        if 'exit typing mode' in query_l or 'end typing mode' in query_l or 'end typing session' in query_l:
            if 'exit typing mode' in query_l:
                speak('Exiting typing mode now sir.')
            elif 'end typing mode' in query_l:
                speak('Ending typing mode now sir.')
            else:
                speak('Ending typing session now sir.')
            break
        else:
            if 'none123' not in query:
                pyautogui.write(query)
            else:
                pass


def read():
    press('control c')
    text = pyperclip.paste()
    speak(text)
