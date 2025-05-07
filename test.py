import asyncio
import websockets
import json
from typing import Optional, Callable, Any, Dict
import logging

class WebSocketConnection:
    def __init__(self, url: str):
        """
        Initialize WebSocket connection.
        
        Args:
            url (str): WebSocket server URL (e.g., 'ws://localhost:8080')
        """
        self.url = url
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
        
    async def connect(self) -> bool:
        """
        Establish WebSocket connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.websocket = await websockets.connect(self.url)
            self.connected = True
            self.logger.info(f"Connected to WebSocket server at {self.url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to WebSocket server: {str(e)}")
            self.connected = False
            return False
            
    async def disconnect(self) -> None:
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            self.logger.info("Disconnected from WebSocket server")
            
    async def send_message(self, message: Dict[str, Any]) -> bool:
        """
        Send a message through the WebSocket connection.
        
        Args:
            message (Dict[str, Any]): Message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.connected or not self.websocket:
            self.logger.error("Not connected to WebSocket server")
            return False
            
        try:
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            return False
            
    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """
        Receive a message from the WebSocket connection.
        
        Returns:
            Optional[Dict[str, Any]]: Received message or None if error
        """
        if not self.connected or not self.websocket:
            self.logger.error("Not connected to WebSocket server")
            return None
            
        try:
            message = await self.websocket.recv()
            return json.loads(message)
        except Exception as e:
            self.logger.error(f"Failed to receive message: {str(e)}")
            return None
            
    async def listen(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Continuously listen for messages and call the callback function.
        
        Args:
            callback (Callable[[Dict[str, Any]], None]): Function to call with received messages
        """
        if not self.connected or not self.websocket:
            self.logger.error("Not connected to WebSocket server")
            return
            
        try:
            while self.connected:
                message = await self.receive_message()
                if message:
                    callback(message)
        except Exception as e:
            self.logger.error(f"Error in message listener: {str(e)}")
            self.connected = False
