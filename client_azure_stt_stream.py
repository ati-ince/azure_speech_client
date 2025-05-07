"""
WORKING: Python 3.12 + websockets==15.0.1
Pass credentials via query params instead of headers
"""

import asyncio
import os
import sys
import urllib.parse

import numpy as np
import sounddevice as sd
import websockets

VERSION = "v0.1.8"

BASE_WS_URI = "ws://localhost:8000/stt"

USERNAME = "demo"
HASHKEY = "demo_hash"
LANG = 'tr-TR' #'en-GB'

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_FRAMES = 1024

# ───── Encode credentials in query string ─────
params = urllib.parse.urlencode({
    "username": USERNAME,
    "hashkey": HASHKEY,
    "lang": LANG
})
WS_URI = f"{BASE_WS_URI}?{params}"

# ───────── Audio sender coroutine ─────────
async def audio_sender(ws):
    loop = asyncio.get_running_loop()

    def callback(indata, _frames, _time, status):
        if status:
            print(status, file=sys.stderr)
        pcm = (indata * 32767).astype(np.int16).tobytes()
        loop.call_soon_threadsafe(lambda: asyncio.create_task(ws.send(pcm)))

    with sd.InputStream(samplerate=SAMPLE_RATE,
                        channels=CHANNELS,
                        dtype="float32",
                        blocksize=CHUNK_FRAMES,
                        callback=callback):
        await asyncio.Future()

# ───────── Text receiver coroutine ─────────
async def text_receiver(ws):
    async for msg in ws:
        print("🡆", msg)

# ───────── Main entry point ─────────
async def main():
    async with websockets.connect(WS_URI, max_size=None) as ws:
        print(f"Connected to {WS_URI}")
        await asyncio.gather(audio_sender(ws), text_receiver(ws))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
