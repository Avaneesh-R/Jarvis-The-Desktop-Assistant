"""
window_manager.py
--------------------
Window and app-launching helpers: switching between windows/Google
accounts, closing windows, refreshing a browser tab, and opening apps
via the Start menu search.
"""

import time
import pyautogui

from speech import speak, takeCommand
from input_control import press


def openapps(query):
    pyautogui.press("super")
    pyautogui.typewrite(query)
    pyautogui.sleep(1.5)
    pyautogui.press('enter')


def switchAccount(query):
    if 'first' in query or 'current' in query:
        pyautogui.hotkey('enter')
    elif 'second' in query:
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')
    elif 'third' in query:
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')
    elif 'forth' in query:
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')
    elif 'fifth' in query:
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')
    elif 'sixth' in query:
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')


def refresh():
    pyautogui.rightClick(1000, 900)
    time.sleep(0.9)
    for i in range(1, 5):
        press('up')
    press('enter')
    pyautogui.leftClick(1300, 780)
    pyautogui.hotkey('f5')
    speak('Once.')
    pyautogui.hotkey('f5')
    speak('Twice.')
    pyautogui.hotkey('f5')
    speak('And done.')


def switchWindow(query):
    if 'next' in query:
        pyautogui.press('tab')
    elif 'previous' in query:
        pyautogui.hotkey('shift')
    elif 'first' in query or 'current' in query:
        pass
    elif 'second' in query:
        pyautogui.press('tab')
    elif 'third' in query:
        pyautogui.press('tab')
        pyautogui.press('tab')
    elif 'fourth' in query:
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
    elif 'fifth' in query:
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
    else:
        speak('Sorry, I can only switch upto 5 windows sir. Please try again.')
        m = takeCommand().lower()
        switchWindow(m)


def closeWindow(query):
    if 'first' in query or 'current' in query:
        speak('Closing the current window now.')
        pyautogui.press('delete')
    elif 'next' in query or 'second' in query:
        pyautogui.press('tab')
        if 'next' in query:
            speak('Closing the next window now.')
        else:
            speak('Closing the second window now.')
        pyautogui.press('delete')
    elif 'previous' in query or 'last' in query:
        if 'previous' in query:
            speak('Closing the previous window sir.')
        else:
            speak('Closing the last window sir.')
        press('shift tab')
        press('delete')
    elif 'third' in query:
        pyautogui.press('tab')
        pyautogui.press('tab')
        speak('Closing the third window now.')
        pyautogui.press('delete')
    elif 'fourth' in query:
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        speak('Closing the forth window now.')
        pyautogui.press('delete')
    elif 'fifth' in query:
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        speak('Closing the fifth window now.')
        pyautogui.press('delete')
    else:
        speak('Sorry sir I can only close upto 5 windows. Please try again.')
        n = takeCommand().lower()
        closeWindow(n)
