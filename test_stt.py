import asyncio
import signal
import sys
from client_azure_stt_class import AzureSTTClient

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

    # Create a single client instance
    client = AzureSTTClient()
    
    try:
        # First run with 10 seconds timeout
        print("\n=== Starting first run (10 seconds) ===")
        asyncio.run(client.run(timeout=10))
        
        # Sleep for 2 seconds between runs
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
        
        # Second run with 15 seconds timeout
        print("\n=== Starting second run (15 seconds) ===")
        asyncio.run(client.run(timeout=15))
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\nCleaning up...")  