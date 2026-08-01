"""
web.py
--------
Browser-related helpers used by commands.py.
"""

import webbrowser

from speech import speak


def searchYoutube(search):
    search = search.replace('jarvis', '')
    search = search.replace('javed', '')
    search = search.replace('search', '')
    search = search.replace('youtube', '')
    search = search.replace('search in', '')
    search = search.replace('search on', '')
    search = search.replace('youtube for', '')
    search = search.replace('youtube about', '')
    search = search.replace('  ', '')
    url = f'https://www.youtube.com/results?search_query={search}'
    chrome_url = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_url))
    webbrowser.get('chrome').open(url)
    speak('Search complete. The results are there on your screen sir')
