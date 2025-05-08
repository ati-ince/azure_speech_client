import asyncio
import signal
import sys
from client_azure_stt_module import AzureSTTClient, AzureSTTTranslationClient

# Create client instances
stt_client = AzureSTTClient()
translation_client = AzureSTTTranslationClient()

async def call_stt(timeout: float = 10, lang: str = 'tr-TR'):
    """Call STT client and return collected text"""
    collected_text = await stt_client.run(timeout=timeout, lang=lang)
    return collected_text

async def call_translation(timeout: float = 10, lang: str = 'tr-TR'):
    """Call STT translation client and return collected translations"""
    collected_translations = await translation_client.run(timeout=timeout, lang=lang)
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
        # Test 1: Basic STT with Turkish
        print("\n=== Test 1: Basic STT (Turkish, 10 seconds) ===")
        collected_text = asyncio.run(call_stt(timeout=10, lang='tr-TR'))
        if 'tr-TR' in collected_text:
            print("\nCollected Turkish text:")
            print(collected_text['tr-TR'])
        
        # Sleep between tests
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
        
        # Test 2: Basic STT with English
        print("\n=== Test 2: Basic STT (English, 10 seconds) ===")
        collected_text = asyncio.run(call_stt(timeout=10, lang='en-GB'))
        if 'en-GB' in collected_text:
            print("\nCollected English text:")
            print(collected_text['en-GB'])
        
        # Sleep between tests
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
        
        # Test 3: STT Translation (Turkish to English)
        print("\n=== Test 3: STT Translation (Turkish to English, 15 seconds) ===")
        translations = asyncio.run(call_translation(timeout=15, lang='tr-TR'))
        if 'tr-TR' in translations:
            print("\nTurkish (Original):")
            print(translations['tr-TR']['transcribed'])
            print("\nEnglish (Translation):")
            print(translations['tr-TR']['translated'])
        
        # Sleep between tests
        print("\nSleeping for 2 seconds...")
        asyncio.run(asyncio.sleep(2))
        
        # Test 4: STT Translation (English to English)
        print("\n=== Test 4: STT Translation (English to English, 15 seconds) ===")
        translations = asyncio.run(call_translation(timeout=15, lang='en-GB'))
        if 'en-GB' in translations:
            print("\nEnglish (Original):")
            print(translations['en-GB']['transcribed'])
            print("\nTurkish (Translation):")
            print(translations['en-GB']['translated'])
        
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\nCleaning up...") 