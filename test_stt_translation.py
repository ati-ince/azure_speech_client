import asyncio
import signal
import sys
from client_azure_stt_translation_class import AzureSTTTranslationClient

client = AzureSTTTranslationClient()

async def call(timeout: float = 10, lang: str = 'tr-TR'):
    collected_translations = await client.run(timeout=timeout, lang=lang)
    return collected_translations
    
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
        # First run with Turkish to English translation (10 seconds)
        print("\n=== Starting Turkish to English translation (10 seconds) ===")
        collected_translations = asyncio.run(call(timeout=10, lang='tr-TR'))
        
        # Print collected translations
        if 'tr-TR' in collected_translations:
            print("\nTurkish (Original):")
            print(collected_translations['tr-TR']['transcribed'])
            print("\nEnglish (Translation):")
            print(collected_translations['tr-TR']['translated'])
        
        # Sleep for 2 seconds between runs
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
        
        # Second run with English to English translation (15 seconds)
        print("\n=== Starting English to English translation (15 seconds) ===")
        collected_translations = asyncio.run(call(timeout=15, lang='en-GB'))
        
        # Print collected translations
        if 'en-GB' in collected_translations:
            print("\nEnglish (Original):")
            print(collected_translations['en-GB']['transcribed'])
            print("\nEnglish (Translation):")
            print(collected_translations['en-GB']['translated'])
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\nCleaning up...") 