"""
STT Client Module for WebSocket-based Speech-to-Text communication
"""

import asyncio
import urllib.parse
import numpy as np
import sounddevice as sd
import websockets
from typing import Optional, Callable

class STTClient:
    def __init__(
        self,
        base_ws_uri: str = "ws://localhost:8000/stt",
        username: str = "demo",
        hashkey: str = "demo_hash",
        lang: str = "tr-TR",
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_frames: int = 1024
    ):
        self.base_ws_uri = base_ws_uri
        self.username = username
        self.hashkey = hashkey
        self.lang = lang
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_frames = chunk_frames
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.is_streaming = False
        self._setup_ws_uri()

    def _setup_ws_uri(self):
        params = urllib.parse.urlencode({
            "username": self.username,
            "hashkey": self.hashkey,
            "lang": self.lang
        })
        self.ws_uri = f"{self.base_ws_uri}?{params}"

    async def _audio_sender(self, on_text: Callable[[str], None]):
        loop = asyncio.get_running_loop()

        def callback(indata, _frames, _time, status):
            if status:
                print(f"Audio callback status: {status}")
            if self.is_streaming:
                pcm = (indata * 32767).astype(np.int16).tobytes()
                loop.call_soon_threadsafe(lambda: asyncio.create_task(self.ws.send(pcm)))

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=self.chunk_frames,
            callback=callback
        ):
            while self.is_streaming:
                await asyncio.sleep(0.1)

    async def _text_receiver(self, on_text: Callable[[str], None]):
        try:
            async for msg in self.ws:
                on_text(msg)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")

    async def start_streaming(self, timeout: float = 10.0, on_text: Callable[[str], None] = print):
        """
        Start streaming audio to the STT server with a timeout.
        
        Args:
            timeout: Streaming duration in seconds
            on_text: Callback function to handle transcribed text
        """
        try:
            self.ws = await websockets.connect(self.ws_uri, max_size=None)
            print(f"Connected to {self.ws_uri}")
            
            self.is_streaming = True
            audio_task = asyncio.create_task(self._audio_sender(on_text))
            text_task = asyncio.create_task(self._text_receiver(on_text))
            
            # Wait for timeout
            await asyncio.sleep(timeout)
            
            # Stop streaming
            self.is_streaming = False
            await audio_task
            await text_task
            
        except Exception as e:
            print(f"Error during streaming: {e}")
        finally:
            if self.ws:
                await self.ws.close()
            self.is_streaming = False

    async def stop_streaming(self):
        """Stop the current audio streaming session."""
        self.is_streaming = False
        if self.ws:
            await self.ws.close() 