"""
Azure Speech-to-Text Client Module
WORKING: Python 3.12 + websockets==15.0.1
Pass credentials via query params instead of headers
"""

import asyncio
import os
import sys
import urllib.parse
from typing import Optional, Callable

import numpy as np
import sounddevice as sd
import websockets

class AzureSTTClient:
    VERSION = "v0.1.8"
    
    def __init__(
        self,
        base_ws_uri: str = "ws://localhost:8000/stt",
        username: str = "demo",
        hashkey: str = "demo_hash",
        lang: str = 'tr-TR',
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_frames: int = 1024,
        on_text_received: Optional[Callable[[str], None]] = None
    ):
        self.base_ws_uri = base_ws_uri
        self.username = username
        self.hashkey = hashkey
        self.lang = lang
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_frames = chunk_frames
        self.on_text_received = on_text_received or (lambda x: print("🡆", x))
        
        # Encode credentials in query string
        params = urllib.parse.urlencode({
            "username": self.username,
            "hashkey": self.hashkey,
            "lang": self.lang
        })
        self.ws_uri = f"{self.base_ws_uri}?{params}"
        
        self._running = False
        self._ws = None

    async def _audio_sender(self, ws):
        loop = asyncio.get_running_loop()

        def callback(indata, _frames, _time, status):
            if status:
                print(status, file=sys.stderr)
            pcm = (indata * 32767).astype(np.int16).tobytes()
            loop.call_soon_threadsafe(lambda: asyncio.create_task(ws.send(pcm)))

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=self.chunk_frames,
            callback=callback
        ):
            await asyncio.Future()

    async def _text_receiver(self, ws):
        async for msg in ws:
            self.on_text_received(msg)

    async def start(self):
        """Start the STT client"""
        if self._running:
            return
            
        self._running = True
        try:
            self._ws = await websockets.connect(self.ws_uri, max_size=None)
            print(f"Connected to {self.ws_uri}")
            await asyncio.gather(
                self._audio_sender(self._ws),
                self._text_receiver(self._ws)
            )
        except Exception as e:
            print(f"Error: {e}")
            self._running = False
            raise

    async def stop(self):
        """Stop the STT client"""
        self._running = False
        if self._ws:
            await self._ws.close()
            self._ws = None

    def run(self):
        """Run the STT client in the main thread"""
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            print("\nStopped by user")
            asyncio.run(self.stop())

# Example usage
# if __name__ == "__main__":
#     client = AzureSTTClient()
#     client.run() 
    
if __name__ == "__main__":
    try:
        client = AzureSTTClient()
        client.run() 
    except KeyboardInterrupt:
        print("\nStopped by user")