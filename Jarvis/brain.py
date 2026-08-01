"""
brain.py
----------
Gives Jarvis an actual conversational ability using the Gemini API.

Instead of only matching fixed voice commands, any query that doesn't match
a known command in jarvis.py falls back to this module, which sends it to
Gemini and returns a short, speakable reply. A single chat session is kept
alive for the whole run, so Jarvis remembers what was said earlier in the
conversation (e.g. "what did I just ask you?").

Requires the GEMINI_API_KEY environment variable to be set.
"""

import os
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """
You are Jarvis, a witty and capable desktop voice assistant, in the spirit of
Tony Stark's J.A.R.V.I.S. You occasionally address the user as "sir", but not
in every single reply. Your replies are converted to speech, so:
- Keep answers short and conversational, ideally 1-3 sentences.
- Never use markdown, bullet points, headers, or emojis.
- Never read out URLs or code unless explicitly asked.
- If a question is genuinely complex, give a brief answer first and ask if
  the user wants you to go deeper, instead of dumping everything at once.
"""

MODEL_NAME = "gemini-3.5-flash"
_client = None
_chat = None

def _ensure_chat():
    """Lazily creates the Gemini client and chat session on first use."""
    global _client, _chat

    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Set it before running Jarvis, e.g.:\n"
                "  setx GEMINI_API_KEY \"your-key-here\"   (Windows, new terminal needed after)"
            )
        _client = genai.Client(api_key=api_key)

    if _chat is None:
        _chat = _client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                # Jarvis is a voice assistant, not a reasoning chatbot: turning
                # thinking off keeps replies fast and avoids the SDK warning
                # about non-text (thought_signature) parts in response.text.
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
    return _chat

def ask(query: str) -> str:
    """Sends `query` to Gemini and returns Jarvis's reply as plain text.

    On any failure (missing key, network issue, API error) this returns a
    friendly spoken fallback instead of raising, so a bad network call
    never crashes the main assistant loop.
    """
    try:
        chat = _ensure_chat()
        response = chat.send_message(query)
        return response.text.strip()
    except Exception as e:
        print(f"[brain.py] Gemini error: {e}")
        return "Sorry sir, I couldn't reach my brain just now. Please try again in a moment."


def reset_conversation():
    """Wipes the running chat history and starts fresh next time ask() is called."""
    global _chat
    _chat = None