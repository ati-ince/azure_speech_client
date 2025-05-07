import asyncio
import signal
import sys
from client_azure_stt_class_v2 import AzureSTTClientV2

client = AzureSTTClientV2()

async def call(timeout: float = 10, lang: str = 'tr-TR'):
    collected_text = await client.run(timeout=timeout, lang=lang)
    return collected_text
    
def signal_handler(signum, frame):
    print("\nReceived signal to stop")
    sys.exit(0)
    
if __name__ == "__main__":
    # Set up signal handlers for Windows
    if sys.platform == 'win32':
        import win32api
        win32api.SetConsoleCtrlHandler(signal_handler, True)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    try:
        # First run with 10 seconds timeout
        print("\n=== Starting first run (10 seconds) ===")
        collected_text = asyncio.run(call(timeout=10,lang='tr-TR'))
        print(collected_text.get('tr-TR', 'No text collected'))
        
        # Sleep for 2 seconds between runs
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
                
        # Second run with 15 seconds timeout
        print("\n=== Starting second run (15 seconds) ===")
        collected_text = asyncio.run(call(timeout=15,lang='en-GB'))
        print(collected_text.get('en-GB', 'No text collected'))
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\nCleaning up...")  