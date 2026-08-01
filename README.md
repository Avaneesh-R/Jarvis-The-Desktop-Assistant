# Jarvis — Desktop Voice Assistant

A wake-word-activated, voice-controlled desktop assistant for Windows, built in Python. Say the wake word, then talk to it — it can control your system, manage windows and apps, search the web, and hold an actual conversation via the Gemini API when a query doesn't match a fixed command.

## Features

**System control**
- Sleep, shutdown, restart, sign out
- Volume up/down, mute
- Screenshots, split screen, maximize/minimize windows

**App & window management**
- Open/close applications
- Switch between and close windows (ordinal-based — "close the third window")
- Close browser tabs by count
- Direct handling for WhatsApp, Telegram, Chrome

**Web**
- Google search, YouTube search
- Gemini web integration

**Productivity**
- Create files (`.txt`, `.ppt`, `.py`)
- Copy, paste, save
- Dictation mode — speech typed out as keystrokes
- Read clipboard contents aloud

**Conversation**
- Falls back to the Gemini API (`brain.py`) for any query that isn't a recognized command, so Jarvis can hold a real back-and-forth instead of only responding to fixed phrases
- Maintains chat history for the session, so it remembers earlier context

**Personality**
- Randomized greetings, thank-yous, and introductions for a more natural feel, instead of the same canned line every time

## Project structure

```
jarvis/
├── jarvis.py        # Main entry point — wake word loop, command router
├── brain.py         # Gemini-powered conversational fallback
├── wakeword.py       # Wake word detection
├── requirements.txt
└── .env.example      # Template for required environment variables
```

The command logic in `jarvis.py` is split into task-category modules that get imported into the main file, rather than living in one large script — this keeps individual files short and each concern isolated.

## Tech stack

| Purpose | Library |
|---|---|
| Speech-to-text | `speech_recognition` (Google Speech API) |
| Text-to-speech | `pyttsx3` (SAPI5) |
| System/UI automation | `pyautogui`, `keyboard` |
| Media/browser automation | `pywhatkit` |
| Conversational AI | Google Gemini API (`google-genai`) |

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd jarvis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key**

   Create a `.env` file (or set the environment variable directly):
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run it**
   ```bash
   python jarvis.py
   ```

5. Say the wake word, wait for the acknowledgment ("Yes sir?"), then speak your command.

## Notes

- Currently built and tested for **Windows** — several commands (`taskkill`, `shutdown.exe`) are Windows-specific.
- No credentials or secrets are stored in source. All keys are read from environment variables.
- The conversational fallback uses `thinking_budget=0` on Gemini calls to keep voice responses fast, since a voice loop needs low latency over deep reasoning.

## Roadmap / possible next steps

- Cross-platform support (macOS/Linux equivalents for system commands)
- Encrypted local storage for any saved credentials, if that feature returns
- Expand the personality layer with more varied response pools
