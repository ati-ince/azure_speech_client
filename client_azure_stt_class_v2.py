"""
WORKING: Python 3.12 + websockets==15.0.1
Pass credentials via query params instead of headers
Class-based implementation with timeout support and text storage
"""

import asyncio
import os
import sys
import urllib.parse
from typing import Optional, Dict

import numpy as np
import sounddevice as sd
import websockets

VERSION = "v0.1.8"

class AzureSTTClientV2:
    def __init__(
        self,
        base_ws_uri: str = "ws://localhost:8000/stt",
        username: str = "demo",
        hashkey: str = "demo_hash",
        lang: str = 'tr-TR',
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
        
        # Encode credentials in query string
        # self.ws_uri = self.uri(lang=self.lang,
        #                        username=self.username,
        #                        hashkey=self.hashkey)
        
        self._ws = None
        self._audio_task = None
        self._text_task = None
        self._running = False
        self.collected_text: Dict[str, str] = {}  # Store text by language code
    
    def uri(self, lang: str = None, username: str = None, hashkey: str = None):
        params = urllib.parse.urlencode({
            "username": username,
            "hashkey": hashkey,
            "lang": lang
        })
        return f"{self.base_ws_uri}?{params}"
    
    async def _audio_sender(self):
        loop = asyncio.get_running_loop()

        def callback(indata, _frames, _time, status):
            if status:
                print(status, file=sys.stderr)
            pcm = (indata * 32767).astype(np.int16).tobytes()
            loop.call_soon_threadsafe(lambda: asyncio.create_task(self._ws.send(pcm)))

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=self.chunk_frames,
            callback=callback
        ):
            while self._running:
                await asyncio.sleep(0.1)

    async def _text_receiver(self):
        async for msg in self._ws:
            # Store text in dictionary instead of printing
            if self.lang not in self.collected_text:
                self.collected_text[self.lang] = ""
            self.collected_text[self.lang] += msg + " "

    async def run(self,
                  timeout: Optional[float] = None,
                  lang: str = None,
                  username: str = None,
                  hashkey: str = None):
        """
        Initialize the STT client with optional parameters.
        If any parameter is provided, it will override the default values.
        """
        if lang is not None:
            self.lang = lang
        if username is not None:
            self.username = username
        if hashkey is not None:
            self.hashkey = hashkey
            
        self.ws_uri = self.uri(lang=self.lang,
                               username=self.username,
                               hashkey=self.hashkey)
        
        """
        Run the STT client with optional timeout in seconds.
        If timeout is None, runs indefinitely until interrupted.
        Returns the collected text dictionary.
        """
        self._running = True
        try:
            async with websockets.connect(self.ws_uri, max_size=None) as self._ws:
                print(f"Connected to {self.ws_uri}")
                self._audio_task = asyncio.create_task(self._audio_sender())
                self._text_task = asyncio.create_task(self._text_receiver())
                
                if timeout is not None:
                    await asyncio.wait_for(
                        asyncio.gather(self._audio_task, self._text_task),
                        timeout=timeout
                    )
                else:
                    await asyncio.gather(self._audio_task, self._text_task)
                    
        except asyncio.TimeoutError:
            print(f"\nStopped after {timeout} seconds timeout")
        except KeyboardInterrupt:
            print("\nStopped by user")
        finally:
            self._running = False
            if self._audio_task:
                self._audio_task.cancel()
            if self._text_task:
                self._text_task.cancel()
            try:
                await asyncio.gather(self._audio_task, self._text_task, return_exceptions=True)
            except Exception:
                pass
            
        return self.collected_text

    def get_collected_text(self) -> Dict[str, str]:
        """Get the collected text dictionary."""
        return self.collected_text 