"""
jarvis.py
-----------
Entry point. Wires the wake-word listener to the command router and
runs the main assistant loop. All actual command logic lives in
commands.py; speech I/O, personality, input control, window
management, and web helpers each live in their own module.
"""

import time
from speech import speak, takeCommand
from personality import wishme
from commands import mainf

if __name__ == "__main__":
    wishme()
    time.sleep(0.8)
    while True:
        query = takeCommand().lower()
        # query = input("Enter your command: ").lower()
        if ' and ' in query:
            L = query.split(sep=' and ')
            x = len(L)
            before = L[0]
            mainf(before)
            if x == 2:
                middle = L[1]
                mainf(middle)
            elif x == 3:
                after = L[2]
                mainf(middle)
                mainf(after)
        else:
            mainf(query)
        time.sleep(0.8)
