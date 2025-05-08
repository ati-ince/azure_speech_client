"""
Class-based implementation of Azure TTS client with proper resource management
"""

import os
import sys
import requests
import pyaudio
from typing import Optional, Dict, Any

VERSION = "v0.2.0"

class AzureTTSClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000/tts",
        username: str = "demo",
        hashkey: str = "demo_hash",
        lang: str = "en-GB",
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024
    ):
        self.base_url = base_url
        self.username = username
        self.hashkey = hashkey
        self.lang = lang
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        
        # PyAudio configuration
        self.format = pyaudio.paInt16
        self._p = None
        self._stream = None
        
    def _setup_audio(self):
        """Initialize PyAudio and create output stream"""
        self._p = pyaudio.PyAudio()
        self._stream = self._p.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            output=True
        )
        
    def _cleanup_audio(self):
        """Clean up PyAudio resources"""
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._p:
            self._p.terminate()
            
    def speak(self, text: str, lang: Optional[str] = None) -> bool:
        """
        Convert text to speech and play it through the default audio device.
        
        Args:
            text: The text to convert to speech
            lang: Optional language override (e.g., 'en-GB', 'tr-TR')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use provided language or default
            target_lang = lang if lang is not None else self.lang
            
            # Prepare request parameters
            params = {
                "text": text,
                "lang": target_lang
            }
            
            headers = {
                "X-Username": self.username,
                "X-Hashkey": self.hashkey
            }
            
            # Setup audio output
            self._setup_audio()
            
            print("🔊 Streaming TTS audio...")
            with requests.get(self.base_url, params=params, headers=headers, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        self._stream.write(chunk)
            print("✅ Finished playback.")
            return True
            
        except Exception as e:
            print(f"Error during TTS playback: {e}", file=sys.stderr)
            return False
            
        finally:
            self._cleanup_audio()
            
    def __enter__(self):
        """Context manager entry"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure cleanup"""
        self._cleanup_audio() 