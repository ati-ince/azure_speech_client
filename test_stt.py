"""
Test script for STT client demonstrating multiple streaming sessions
"""

import asyncio
from stt_client import STTClient
from typing import List

class TextCollector:
    def __init__(self):
        self.responses: List[str] = []
    
    def __call__(self, text: str):
        """Handle incoming transcribed text"""
        self.responses.append(text)
        print(f"🡆 {text}")
    
    def get_all_responses(self) -> List[str]:
        return self.responses

async def main():
    # Create STT client instance
    client = STTClient(
        username="demo",
        hashkey="demo_hash",
        lang="tr-TR"
    )
    
    # Create a text collector to store all responses
    text_collector = TextCollector()
    
    try:
        # First streaming session (5 seconds)
        print("\n=== Starting first streaming session (5 seconds) ===")
        await client.start_streaming(timeout=5.0, on_text=text_collector)
        
        # Print summary of first session
        print("\nFirst session responses:")
        for response in text_collector.get_all_responses():
            print(f"  - {response}")
        
        # Clear responses for next session
        text_collector.responses.clear()
        
        # Wait 2 seconds between sessions
        print("\nWaiting 2 seconds before next session...")
        await asyncio.sleep(2)
        
        # Second streaming session (3 seconds)
        print("\n=== Starting second streaming session (3 seconds) ===")
        await client.start_streaming(timeout=3.0, on_text=text_collector)
        
        # Print summary of second session
        print("\nSecond session responses:")
        for response in text_collector.get_all_responses():
            print(f"  - {response}")
        
        # Clear responses for next session
        text_collector.responses.clear()
        
        # Wait 2 seconds between sessions
        print("\nWaiting 2 seconds before next session...")
        await asyncio.sleep(2)
        
        # Third streaming session (4 seconds)
        print("\n=== Starting third streaming session (4 seconds) ===")
        await client.start_streaming(timeout=4.0, on_text=text_collector)
        
        # Print summary of third session
        print("\nThird session responses:")
        for response in text_collector.get_all_responses():
            print(f"  - {response}")
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure we stop any ongoing streaming
        await client.stop_streaming()

if __name__ == "__main__":
    asyncio.run(main()) 