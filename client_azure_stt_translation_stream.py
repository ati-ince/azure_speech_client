"""
Mic → /stt-translation → prints {transcribed, translated}
Works with same username/hashkey + lang query param.
"""

import asyncio
import json
import os
import sys
import urllib.parse

import numpy as np
import sounddevice as sd
import websockets

VERSION = "v0.1.8"

BASE_WS_URI = "ws://localhost:8000/stt-translation"
USERNAME = "demo"
HASHKEY = "demo_hash"
LANG = "en-GB" #"tr-TR" # for example Turkish to English

params = urllib.parse.urlencode({"username": USERNAME, "hashkey": HASHKEY, "lang": LANG})
WS_URI = f"{BASE_WS_URI}?{params}"

SAMPLE_RATE = 16000
CHUNK_FRAMES = 1024

async def audio_sender(ws):
    loop = asyncio.get_running_loop()

    def cb(indata, _frames, _time, status):
        if status:
            print(status, file=sys.stderr)
        ws_pcm = (indata * 32767).astype(np.int16).tobytes()
        loop.call_soon_threadsafe(lambda: asyncio.create_task(ws.send(ws_pcm)))

    with sd.InputStream(samplerate=SAMPLE_RATE,
                        channels=1,
                        dtype="float32",
                        blocksize=CHUNK_FRAMES,
                        callback=cb):
        await asyncio.Future()

async def text_receiver(ws):
    async for msg in ws:
        try:
            payload = json.loads(msg)
            print(f"🡆 transcribed: {payload['transcribed']}")
            print(f"   translated : {payload['translated']}\n")
        except json.JSONDecodeError:
            print("Received non‑JSON:", msg)

async def main():
    async with websockets.connect(WS_URI, max_size=None) as ws:
        print("Connected. Speak…")
        await asyncio.gather(audio_sender(ws), text_receiver(ws))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
