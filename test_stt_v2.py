import asyncio
import signal
import sys
from client_azure_stt_class_v2 import AzureSTTClientV2

def signal_handler(signum, frame):
    print("\nReceived signal to stop")
    sys.exit(0)

async def main():
    # Create a client instance with Turkish language
    client_tr = AzureSTTClientV2(lang='tr-TR')
    
    try:
        # Run with 10 seconds timeout
        print("\n=== Starting Turkish STT (10 seconds) ===")
        collected_text = await client_tr.run(timeout=10)
        
        # Print collected text after timeout
        print("\nCollected Turkish text:")
        print(collected_text.get('tr-TR', 'No text collected'))
        
        # Create another client instance with English language
        client_en = AzureSTTClientV2(lang='en-GB')
        
        # Run with 15 seconds timeout
        print("\n=== Starting English STT (15 seconds) ===")
        collected_text = await client_en.run(timeout=15)
        
        # Print collected text after timeout
        print("\nCollected English text:")
        print(collected_text.get('en-GB', 'No text collected'))
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\nCleaning up...")

if __name__ == "__main__":
    # Set up signal handlers for Windows
    if sys.platform == 'win32':
        import win32api
        win32api.SetConsoleCtrlHandler(signal_handler, True)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    # Run the main async function
    asyncio.run(main()) 