"""
Play TTS from server with the same credentials & language settings.
"""

import os
import sys
import requests
import pyaudio

# ---------- config ----------

VERSION = "v0.1.8"


TEXT = (
    "Welcome to our text-to-speech demonstration. This short paragraph is "
    "designed to test clarity, pronunciation, and streaming performance."
)
LANG = "en-GB"  # e.g. en-US, tr-TR, fr-FR

params = {"text": TEXT, 
          "lang": LANG}

url = "http://localhost:8000/tts"

headers = {
    "X-Username": "demo",
    "X-Hashkey": "demo_hash"
}

# ---------- PyAudio output ----------
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)

try:
    print("🔊 Streaming TTS audio …")
    with requests.get(url, params=params, headers=headers, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                stream.write(chunk)
    print("✅ Finished playback.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
