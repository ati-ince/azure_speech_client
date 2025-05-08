import signal
import sys
from client_azure_tts_class import AzureTTSClient

def signal_handler(signum, frame):
    print("\nReceived signal to stop")
    sys.exit(0)

def main():
    # Set up signal handlers for Windows
    if sys.platform == 'win32':
        import win32api
        win32api.SetConsoleCtrlHandler(signal_handler, True)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    # Example texts for different languages
    texts = {
        'en-GB': (
            "Welcome to our text-to-speech demonstration. "
            "This is a test of the English voice synthesis."
        ),
        'tr-TR': (
            "Merhaba! Bu bir Türkçe metin okuma testidir. "
            "Ses sentezi sisteminin çalışmasını test ediyoruz."
        )
    }

    try:
        # Create TTS client instance
        tts = AzureTTSClient()
        
        # Test English TTS
        print("\n=== Testing English TTS ===")
        success = tts.speak(texts['en-GB'], lang='en-GB')
        if success:
            print("English TTS completed successfully")
        
        # Test Turkish TTS
        print("\n=== Testing Turkish TTS ===")
        success = tts.speak(texts['tr-TR'], lang='tr-TR')
        if success:
            print("Turkish TTS completed successfully")
            
        # Example using context manager
        print("\n=== Testing with context manager ===")
        with AzureTTSClient() as tts:
            success = tts.speak(texts['en-GB'])
            if success:
                print("Context manager test completed successfully")
                
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\nCleaning up...")

if __name__ == "__main__":
    main() 