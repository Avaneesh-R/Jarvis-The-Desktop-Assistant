"""
wakeword.py
-------------
Always-on, offline wake-word ("hotword") detection for Jarvis, using
openWakeWord: a free, fully open-source wake-word engine (Apache licensed,
no account, no API key, no usage limits). It ships a pretrained "hey_jarvis"
model that is downloaded automatically the first time it runs, then cached
locally.

(An earlier version of this module used Picovoice's Porcupine engine, but
Picovoice discontinued its free tier on June 30, 2026, so this now uses
openWakeWord instead, which has no such restriction.)

Note: the pretrained model is trained on the phrase "hey jarvis", not just
"jarvis" alone. Saying "jarvis" by itself will often still work, but with a
higher chance of being missed — say "Hey Jarvis" for the most reliable
detection.

Flow:
    1. wait_for_wakeword() blocks until "Hey Jarvis" is detected.
    2. It releases the microphone immediately after detecting the wake word,
       so jarvis.py's own takeCommand() (which uses Google Speech Recognition
       through speech_recognition/PyAudio) can grab the mic cleanly for the
       actual command, without the two engines fighting over the audio device.

Requires:
    pip install openwakeword pyaudio numpy
"""

import numpy as np
import pyaudio
import openwakeword
from openwakeword.model import Model

WAKE_PHRASE = "jarvis"
MODEL_NAME = "hey_jarvis"
THRESHOLD = 0.5

RATE = 16000
CHUNK = 1280  # ~80ms of audio; the frame size openWakeWord expects per call

_model = None
_models_downloaded = False


def _ensure_model():
    """Lazily downloads (first run only) and loads the wake-word model."""
    global _model, _models_downloaded
    if not _models_downloaded:
        openwakeword.utils.download_models()
        _models_downloaded = True
    if _model is None:
        _model = Model(wakeword_models=[MODEL_NAME])
    return _model


def wait_for_wakeword():
    """Blocks until the wake phrase is detected, then returns.

    Opens the microphone fresh each call and always releases it before
    returning (even on error), so it never holds the audio device longer
    than it needs to, and takeCommand()'s own mic access doesn't conflict.
    """
    model = _ensure_model()
    model.reset()  # clear any lingering prediction state from a previous call

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    print(f"Listening for wake word '{WAKE_PHRASE}'...")
    try:
        while True:
            raw_chunk = stream.read(CHUNK, exception_on_overflow=False)
            chunk = np.frombuffer(raw_chunk, dtype=np.int16)
            prediction = model.predict(chunk)
            if prediction.get(MODEL_NAME, 0.0) > THRESHOLD:
                print("Wake word detected!")
                return
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def cleanup():
    """Kept for symmetry with the rest of jarvis.py's shutdown path.

    openWakeWord doesn't hold any resource that needs explicit release
    between runs, so there's nothing to do here.
    """
    pass
