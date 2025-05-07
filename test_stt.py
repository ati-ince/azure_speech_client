"""
Test script for STT client demonstrating multiple streaming sessions
"""

import asyncio
from stt_client import STTClient

async def text_handler(text: str):
    """Handle incoming transcribed text"""
    print(f"🡆 {text}")

async def main():
    # Create STT client instance
    client = STTClient(
        username="demo",
        hashkey="demo_hash",
        lang="tr-TR"
    )
    
    try:
        # First streaming session (5 seconds)
        print("\n=== Starting first streaming session (5 seconds) ===")
        await client.start_streaming(timeout=5.0, on_text=text_handler)
        
        # Wait 2 seconds between sessions
        print("\nWaiting 2 seconds before next session...")
        await asyncio.sleep(2)
        
        # Second streaming session (3 seconds)
        print("\n=== Starting second streaming session (3 seconds) ===")
        await client.start_streaming(timeout=3.0, on_text=text_handler)
        
        # Wait 2 seconds between sessions
        print("\nWaiting 2 seconds before next session...")
        await asyncio.sleep(2)
        
        # Third streaming session (4 seconds)
        print("\n=== Starting third streaming session (4 seconds) ===")
        await client.start_streaming(timeout=4.0, on_text=text_handler)
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure we stop any ongoing streaming
        await client.stop_streaming()

if __name__ == "__main__":
    asyncio.run(main()) 