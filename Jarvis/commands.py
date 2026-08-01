"""
commands.py
-------------
The command router. mainf(query) is called once per recognized voice
command and checks it against every command Jarvis knows, in priority
order — more specific phrases are checked before generic ones (e.g.
"sleep the computer" is checked before the bare "sleep" that puts
Jarvis itself to sleep). Anything that matches nothing falls through
to brain.ask(), which hands it to Gemini as an open conversational
question.

This function is intentionally kept as one big if/elif chain rather
than split further into per-category files: many branches share
overlapping keywords ("sleep", "close", "search"...), so the checking
order matters. Splitting it into separately-called category functions
would risk silently changing which branch wins for an ambiguous
phrase, so that refactor is left as a deliberate, testable follow-up
rather than done blindly here.
"""

import os
import time
import datetime
import webbrowser
import keyboard
import pyautogui
import brain
import speech
from speech import speak, takeCommand
from personality import introduce
from input_control import press, Type, typeAndEnter, typingMode, read
from window_manager import switchAccount, switchWindow, closeWindow, refresh, openapps
from web import searchYoutube
from wakeword import wait_for_wakeword

def mainf(query):
    # 1. Telling today's time and date.
    if 'time' in query and 'now' in query:
        strt= datetime.datetime.now().strftime("%I:%M")
        speak(f"Sir now the time is {strt}")
    elif ('day' in query or 'date' in query) and 'today' in query and 'weather' not in query:
        speak(f'Todays date is {datetime.datetime.now().date()} and today is a {datetime.datetime.today().strftime("%A")} sir. ')                      
    # 2. Simply types whatever you say or enters it if the 'enter' hotward is used.
    elif 'typing mode' in query or 'start typing' in query:
        speak('Entering typing mode now sir.')
        speech.r.pause_threshold + 10
        typingMode()
    elif 'enter ' in query and "password" not in query:
        speak("Ok sir...")
        typeAndEnter(query)               
    elif 'type ' in query and 'password' not in query:
        speak("Ok sir...")
        Type(query)
    # 3. Put your computer to sleep, shutdown, sign out or even restart your computer using Jarvis.
    elif 'shut' in query and 'down' in query and ('computer' in query or 'pc' in query or 'system' in query):
            speak('Putting your computer to sleep sir...Thanks for your time...')
            pyautogui.hotkey('win','x')
            time.sleep(0.3)
            pyautogui.hotkey('u')
            time.sleep(0.3)
            pyautogui.hotkey('u') 
            exit()
    elif 'sleep' in query and ('computer' in query or 'pc' in query or 'system' in query):
        speak('Putting your computer to sleep sir...Thanks for your time...')
        pyautogui.hotkey('win','x')
        time.sleep(0.3)
        pyautogui.hotkey('u')
        time.sleep(0.3)
        pyautogui.hotkey('s') 
        exit()
    elif 'sign out' in query and ('computer' in query or 'pc' in query or 'system' in query):
        speak('Signing out from this account...Thanks for your time sir.')
        pyautogui.hotkey('win','l')
        exit()
    elif 'restart' in query and ('computer' in query or 'pc' in query or 'system' in query):
        speak("Restarting the computer. Thanks for your time sir.")
        pyautogui.hotkey('win','x')
        time.sleep(0.3)
        pyautogui.hotkey('u')
        time.sleep(0.3)
        pyautogui.hotkey('r') 
        exit()
    elif 'sleep' in query:
        speak('Putting Jarvis to sleep now sir.')
        wait_for_wakeword()
        speak("Yes sir?")
    # 4. Refresh your system.
    elif 'refresh' in query:
        speak('Running three stages of refreshing the system now.')
        refresh()        
    # 5. Change your google account.
    elif ('switch' in query  or 'change' in query) and 'account' in query:
        if google_is_open==1:
            speak("Alright sir...")
            pyautogui.hotkey('ctrl','shift','m')
            speak('Which account do you want me to change it to sir ?')
            l= takeCommand()
            m= l.lower()
            switchAccount(m)
            speak("Changing your account now sir.")
        else:
            speak("Alright sir...")
            webbrowser.open('www.google.com')
            time.sleep(1.5)
            pyautogui.hotkey('ctrl','shift','m')
            speak('Which account do you want me to change it to sir ?')
            l= takeCommand()
            m= l.lower()
            speak("Changing your account now sir.")
            switchAccount(m)
            speak('Account changed successfully.')        
    # 6. Whatsapp controls.
    elif 'open whatsapp' in query:
        chrome_url = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        webbrowser.register('chrome',None, webbrowser.BackgroundBrowser(chrome_url))
        webbrowser.get('chrome').open('web.whatsapp.com')
        speak("Opening whatsapp now sir...")  
    # 7. Weather forecast.
    elif 'weather' in query:
        openapps('weather')
        time.sleep(5)
        speak('Weather forecast should now be on your screen sir.')
    # 8. Playing games.
    elif 'my game' in query:
        speak('Opening your game now sir...')
        openapps('CombatMaster')
    # 9. Google controls.
    elif 'open google' in query:
        speak("Google coming up right away sir...")
        os.system('start chrome.exe')
        google_is_open = 1
    elif ('search for the word' in query or ('find' in query and 'page' in query)):
        query = query.replace('jarvis','')
        query = query.replace('javed','')
        query = query.replace('search for the word','')
        query = query.replace('search this page for','')
        query = query.replace('search the page for','')
        query = query.replace('the word','')
        query = query.replace('the words','')
        query = query.replace('the phrase','')
        query = query.replace('the line','')
        query = query.replace('in the webpage','')
        query = query.replace('in this webpage','')
        query = query.replace('in this page','')
        query = query.replace('in this web page','')
        query = query.replace('in the web page','')
        query = query.replace('find','')
        speak('Ok sir. Searching the web page now.') 
        press('ctrl f')
        Type(query)
    elif 'close google' in query:
        speak("Closing google now sir...")
        os.system("taskkill /f /im chrome.exe")
        google_is_open = 0
    # 10. Youtube controls.
    elif 'open youtube' in query:
        speak("Youtube coming up right away sir.")
        webbrowser.open('www.youtube.com')
    elif 'search' in query and 'youtube' in query:
        webbrowser.open('www.youtube.com')
        time.sleep(3)
        searchYoutube(query)
        youtube_is_open=1
    elif 'close youtube' in query:
        speak("Closing youtube now sir. ")
        pyautogui.hotkey('ctrl','w')
    # 11. Search for apps in the system.
    elif 'search' in query:
        query = query.replace('jarvis','')
        query = query.replace('javed','')
        query = query.replace('search','')
        query = query.replace('computer','')
        query = query.replace('system','')
        query = query.replace('pc','')
        query = query.replace(' for ','')
        query = query.replace('for the file ','')
        pyautogui.press('super')
        time.sleep(0.01)
        pyautogui.typewrite(query)
        speak("This is what I found on your system sir.")        
    # 12. Closing google tabs.
    elif 'close' in query and ('tab' in query or 'times' in query):
        D= { 'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9', 'ten':'10', 'eleven':'11', 'twelve':'12', 'thirteen':'13', 'fourteen':'14', 'fifteen':'15', 'sixteen':'16', 'seventeen':'17', 'eighteen':'18', 'nineteen':'19', 'twenty':'20', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9', '10':'10', '11':'11', '12':'12', '13':'13', '14':'14', '15':'15', '16':'16', '17':'17', '18':'18', '19':'19', '20':'20'}
        query= query.replace('jarvis','')
        query= query.replace('javed','')
        query= query.replace('close','')
        query= query.replace('tabs','')
        query= query.replace('times','')
        query= query.replace('tab','')
        query= query.replace('please','')
        query= query.replace('for me','')
        query= query.replace('now','')
        query= query.replace(' ','')
        for num in D.keys():
            if num==query:
                a = D[num]
        b= int(a)
        if b==1:
            speak('Closing one tab now sir.')
        else:
            speak(f'Closing {b} tabs now sir.')
        for i in range(b):
            time.sleep(0.05)
            press('control w') 
    elif 'one more tab' in query and 'close' in query:
        speak("Closing now...")
        pyautogui.hotkey("ctrl","w")
    # 13. Window management controls.
    elif 'close code' in query:
        os.system(f"taskkill /f /im code.exe")
        speak("Closing VS Code now sir.")
    elif 'close' in query and ('microsoft word' in query or 'word' in query):
        os.system(f"taskkill /f /im winword.exe")
        speak('Closing microsoft word now sir.')
    elif 'close' in query and 'powerpoint' in query:
        os.system(f"taskkill /f /im powerpnt.exe")
        speak('Closing powerpoint now sir.')
    elif 'close' in query and ('chrome' in query or "google" in query):  
        os.system(f"taskkill /f /im chrome.exe")
        speak('Closing chrome now sir.')
    elif 'maximize' in query:
        pyautogui.hotkey('super','up')
        speak('Window maximized on your screen sir.')
    elif 'minimize' in query or 'minimise' in query:
        pyautogui.hotkey('super','down')
        pyautogui.hotkey('super','down')
        speak('Window minimized to the taskbar sir.')
    elif 'close' in query and ('next' in query or 'previous' in query or 'last' in query):
        keyboard.press('alt')
        keyboard.press('tab')
        keyboard.release('tab')
        pyautogui.hotkey('shift','tab')
        if 'next' in query:
            closeWindow('next')
        else:
            closeWindow('previous')
        keyboard.release('alt')            
    elif 'close' in query and ('the window' in query or 'this window' in query or 'the current window' in query):
            keyboard.press('alt')
            keyboard.press('tab')
            keyboard.release('tab')
            pyautogui.hotkey('shift','tab')
            closeWindow('first')
            keyboard.release('alt')
    elif 'close' in query and 'window' in query:
            keyboard.press('alt')
            keyboard.press('tab')
            keyboard.release('tab')
            pyautogui.hotkey('shift','tab')
            speak('Which one sir ?')
            n = takeCommand().lower()
            closeWindow(n)
            keyboard.release('alt')
    elif ('move' in query or 'put' in query) and 'window' in query:
        if 'right' in query:
            pyautogui.hotkey('super','right')
        elif 'left' in query:
            pyautogui.hotkey('super','left')
        else:
            pass
    elif 'split screen' in query:
        keyboard.press('alt')
        keyboard.press('tab')
        keyboard.release('tab')
        pyautogui.hotkey('shift','tab')
        speak("Alright. What is the first window sir ?")
        x = takeCommand().lower()
        switchWindow(x)
        keyboard.release('alt')
        time.sleep(0.25)
        pyautogui.hotkey('super','up')
        pyautogui.hotkey('super','up')
        pyautogui.hotkey('super','left')
        time.sleep(0.25)
        keyboard.press('alt')
        keyboard.press('tab')
        keyboard.release('tab')
        pyautogui.hotkey('shift','tab')
        speak("Ok. And the second one sir ?")
        y = takeCommand().lower()
        switchWindow(y)
        keyboard.release('alt')
        time.sleep(0.25)
        pyautogui.hotkey('super','up')
        pyautogui.hotkey('super','up')
        pyautogui.hotkey('super','right')
        speak('Done sir.')
    # 14. File operations using Jarvis.
    elif 'close' in query and 'file' in query:
        pyautogui.hotkey('alt','f4')
        if 'file' in query:
            speak('File is closed sir.')
        elif 'window' in query:
            speak('Window is closed sir.')
    elif 'save' in query:
        pyautogui.hotkey('ctrl','s')
        speak("Data in the file is saved sir.")        
    # 15. Take a photo from camera.
    elif 'click a photo' in query or 'click my photo' in query:
        speak('Alright sir....')
        os.system('start microsoft.windows.camera:')
        time.sleep(0.7)
        speak('Clicking your photo in...')
        speak('3')
        speak('2')
        speak('1')
        pyautogui.hotkey('enter')
    # 16. Introduction.
    elif 'introduce' in query or 'who are you' in query:
        introduce()
    elif 'what is your name' in query:
        speak('My name is Jarvis sir.')
    # 17. Create a new text file in desktop.
    elif 'create' in query and 'file' in query:
        speak('Ok. What should its name be sir ?')
        name = takeCommand().lower()
        if 'word' in query or 'world' in query:
            f= open(f'C:\\Users\\avane\\OneDrive\\Desktop\\j-files\\{name}.word','w')
        elif 'text' in query or 'notepad' in query:
            f= open(f'C:\\Users\\avane\\OneDrive\\Desktop\\j-files\\{name}.txt','w')
        elif 'powerpoint' in query:
            f= open(f'C:\\Users\\avane\\OneDrive\\Desktop\\j-files\\{name}.ppt','w')
        elif 'python' in query:
            f= open(f'C:\\Users\\avane\\OneDrive\\Desktop\\j-files\\{name}.py','w')
        f.close()
        speak('Document created sir.')
    # 18. Exit from the program.
    elif 'exit' in query:
        speak('Exiting now sir...Thanks for your time...')
        exit()
    elif 'copy' in query:
        press('control c')
        speak('Text copied sir.')
    elif 'paste' in query:
        press('control v')
        speak('Text pasted sir.')
    # 19. Volume controls.
    elif 'volume' in query:
        if 'up' in query or 'increase' in query:
            if 'percent' in query or '%' in query:
                query = query.replace('jarvis','') 
                query = query.replace('javed','') 
                query = query.replace('increase','') 
                query = query.replace('volume','') 
                query = query.replace('up','') 
                query = query.replace('percent','') 
                query = query.replace('the','') 
                query = query.replace('by','') 
                query = query.replace('%','') 
                query = query.replace(' ','')
                percent = int(query)
                times = int(percent / 2)
                speak(f'Increasing the volume by {percent} percent sir.')
                for i in range(times):
                    press('volumeup')  
            else:
                speak('Increasing the volume by 10 percent sir.')
                for i in range(5):
                    press('volumeup')    
        elif 'down' in query or 'decrease' in query:
            if 'percent' in query or '%' in query:
                query = query.replace('jarvis','') 
                query = query.replace('javed','') 
                query = query.replace('decrease','') 
                query = query.replace('volume','') 
                query = query.replace('down','') 
                query = query.replace('percent','') 
                query = query.replace('the','') 
                query = query.replace('by','') 
                query = query.replace('%','') 
                query = query.replace(' ','')
                percent = int(query)
                times = int(percent / 2)
                speak(f'Decreasing the volume by {percent} percent sir.')
                for i in range(times):
                    press('volumedown')  
            else:
                speak('Decreasing the volume by 10 percent sir.')
                for i in range(5):
                    press('volumedown')  
    elif 'mute' in query:
        press('volumemute')
    # 20. Opening a file from the system.        
    elif 'open' in query and 'folder' in query:
        query = query.split(sep='open ')
        speak(f'Searching for {query[1]} folder now.')
        press('super')
        Type(query[1])
        press('up')
        for i in range(1,5):
            press('right')
        for i in range(1,4):
            press('enter')
        speak('This is what I found on your computer sir.')
    elif 'open' in query:
        query = query.split(sep='open ')
        speak(f"Opening {query[1]} now sir.")                         
        openapps(query[1])
    # 21. Read ability.
    elif 'read' in query:
        speak('Ok sir.')
        read()
    elif 'repeat' in query:
        speak('Ok sir.')
        read()
    # 22. System Controls. TODO: Add more system controls.
    elif 'clipboard' in query:
        press('super v')
        speak('This is what is present in your clipboard sir.')  
    elif 'scan' in query:
        openapps('virus and threat protection')
        time.sleep(1)
        speak('Running quick scan for your system now sir.')
        time.sleep(1)
        press('enter')
    # 23. Talk like a person.
    else:
        reply = brain.ask(query)
        print(f"Jarvis: {reply}")
        speak(reply)
